from datetime import date, datetime
import logging
import re

from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    col, sum as spark_sum, date_trunc, to_timestamp,
    lit
)

import ingest
from ingest.datasource_config import S3_SUFFIX

logger = logging.getLogger(__name__)


def psv_filter_to_sql(session, file_schema, input_path: str,
                      output_table: str, filter_date: date,
                      target_jdbc: str) -> DataFrame:
    """
    Read PSV-formatted data and output the results to SQL after
    filtering the input on `filter_date`.

    Usage:
    ```
        simple_schema = StructType([
            StructField('object', StringType(), nullable=True),
            StructField('client_id', StringType(), nullable=True),
            StructField('count', IntegerType(), nullable=True),
            StructField('extraction_date', TimestampType(), nullable=True),
        ])

        psv_to_sql(spark,
                   file_schema=simple_schema,
                   input_path='s3a://my_bucket/data_dump_20210426.gz',
                   output_table='stage.data_dump')
    ```

    TODO: Can you use SELECT * from a jdbc source?
    - https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#run-sql-on-files-directly
    ```
    df = spark.sql("SELECT * FROM parquet.`examples/users.parquet`")
    ```
    TODO: Fine-tune the number of partitions. In general, the recommendation
    is to use a multiple of the number of Spark workers.

    :param session: the Spark session
    :param file_schema: the schema struct array
    :param input_path: the remote data lake path (s3a://, wasbs://, etc.)
    :param output_table: the target SQL table (schema.table)
    :param filter_date: date value to filter input
    :param target_jdbc: sql target (connection string)
    :return: pyspark.sql.DataFrame
    """
    logger.info(f"Read PSV file: {input_path}")

    # Compare to fluent verbose pattern:
    # DataFrameReader.format(args).option("key", "value").schema(args).load()
    file_df = (session
               .read
               .csv(input_path, sep='|', header=False, schema=file_schema)
               .where((col("extraction_date") > filter_date))
               .repartition(8)
               )
    file_df.createOrReplaceTempView("vw_extraction_summary")

    logger.info(f"Grouped summary, filtered > {filter_date}")

    # Spark SQL API
    counts_df = session.sql("""
        SELECT  object as section,
                date_trunc('day', extraction_date) as extraction_day,
                SUM(count) as record_count
        FROM    vw_extraction_summary
        GROUP BY object, date_trunc('day', extraction_date)
        ORDER BY extraction_day DESC, section
    """)
    # DataFrame API
    # counts_df = (file_df
    #              .withColumnRenamed("object", "section")
    #              .withColumn("extraction_day", date_trunc('day', 'extraction_date'))
    #              .select('section', 'extraction_day', 'count')
    #              .groupBy('section', 'extraction_day')
    #              .agg(spark_sum('count').alias("record_count"))
    #              )
    counts_df.show(n=21, truncate=False)

    logger.info(f"Write to SQL: {output_table}")

    (counts_df
     .write
     .option('numPartitions', '8')
     .jdbc(url=target_jdbc, table=output_table, mode='overwrite')
     )

    # Typical fluent verbose patterns:
    # DataFrameWriter.format(args).option(args).bucketBy(args).partitionBy(args).save(path)
    # DataFrameWriter.format(args).option(args).sortBy(args).saveAsTable(table)
    #
    # (file_df
    #  .write
    #  .mode('overwrite')
    #  .format("jdbc")
    #  .option("url", os.environ['TARGET_JDBC_URL'])
    #  .option("dbtable", output_table)
    #  .save()
    #  )

    return counts_df


def psv_to_sql(session, file_schema, input_path: str,
               output_table: str, target_jdbc: str) -> None:
    """
    Read PSV-formatted data and output the results to SQL.

    Usage:
    ```
        simple_schema = StructType([
            StructField('object', StringType(), nullable=True),
            StructField('client_id', StringType(), nullable=True),
            StructField('count', IntegerType(), nullable=True),
            StructField('extraction_date', TimestampType(), nullable=True),
        ])

        psv_to_sql(spark,
                   file_schema=simple_schema,
                   input_path='s3a://my_bucket/data_dump_20210426.gz',
                   output_table='stage.data_dump')
    ```

    TODO: Can you use SELECT * from a jdbc source?
    - https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#run-sql-on-files-directly
    ```
    df = spark.sql("SELECT * FROM parquet.`examples/users.parquet`")
    ```

    :param session: the Spark session
    :param file_schema: the schema struct array
    :param input_path: the remote data lake path (s3a://, wasbs://, etc.)
    :param output_table: the target SQL table (schema.table)
    :param target_jdbc: sql target (connection string)
    :return: None
    """
    logger.info(f"Read PSV file: {input_path}")

    file_df = (session
               .read
               .csv(input_path, sep='|', header=False, schema=file_schema)
               .repartition(8)
               )

    logger.info(f"Write to SQL: {output_table}")

    load_date = re.sub(r"rh_(?P<dt>\d+).gz", "\g<dt>", S3_SUFFIX, re.I)

    # Creates a table with given schema
    (file_df
     .withColumn("created_on", to_timestamp(lit(load_date), "yyyyMMdd"))
     .write
     .option('numPartitions', '8')
     .jdbc(url=target_jdbc,
           table=output_table,
           mode='append')
     )


def psv_to_parquet(session, file_schema, input_path: str,
                   output_path: str) -> None:
    """
    Read PSV-formatted data and output the results to parquet.
    """
    logger.info(f"Read PSV file")

    file_df = (session
               .read
               .csv(input_path,
                    sep='|', header=False, schema=file_schema)
               )

    logger.info(f"Write to parquet")

    # (file_df
    #  .write
    #  .format("parquet")
    #  .mode("overwrite")
    #  .save(output_path)
    #  )

    # Verbose--
    (file_df
     # .limit(21)
     .write
     .parquet(path=output_path, mode="overwrite")
     )


def csv_to_parquet(session, file_schema, input_path: str,
                   output_path: str) -> None:
    """
    Read CSV-formatted data and output the results to parquet.
    """
    logger.info(f"Read CSV file")

    file_df = (session
               .read
               .csv(input_path, header=True, schema=file_schema)
               )

    logger.info(f"Write to parquet")

    (file_df
     # .limit(21)
     .write
     .parquet(path=output_path, mode="overwrite")
     )


def csv_to_json(session, file_schema, input_path: str, output_path: str) -> None:
    """
    Read CSV-formatted data and output the results to json.
    """
    logger.info(f"Read CSV file")

    file_df = (session
               .read
               .csv(input_path, header=True, schema=file_schema)
               )

    logger.info(f"Write to json")

    (file_df
     # .limit(21)
     .write
     .json(path=output_path, mode="overwrite")
     )


def csv_to_sql(session, file_schema, input_path: str,
               output_table: str, target_jdbc: str) -> None:
    """
    Read CSV-formatted data and output the results to SQL.

    :param session: the Spark session
    :param file_schema: the schema struct array
    :param input_path: the remote data lake path (s3a://, wasbs://, etc.)
    :param output_table: the target SQL table (schema.table)
    :param target_jdbc: sql target (connection string)
    :return: None
    """
    logger.info(f"Read CSV file: {input_path}")

    file_df = (session
               .read
               .csv(input_path, header=True, schema=file_schema)
               )

    logger.info(f"Write to SQL: {output_table}")

    # Creates a table with given schema
    (file_df
     # .limit(21)
     .withColumn("created_on",
                 to_timestamp(lit(datetime.now()), "yyyyMMdd"))
     .write
     .jdbc(url=target_jdbc,
           table=output_table,
           mode='append')
     )


def from_csv(session, file_schema, input_path: str) -> DataFrame:
    """
    Read CSV-formatted data.

    :param session: the Spark session
    :param file_schema: the schema struct array
    :param input_path: the remote data lake path (s3a://, wasbs://, etc.)
    :return: DataFrame
    """
    logger.info(f"Read CSV file: {input_path}")

    return (session
            .read
            .csv(input_path, header=True, schema=file_schema)
            )


def from_json(session, file_schema, input_path: str) -> DataFrame:
    """
    Read single-line JSON-formatted data.

    :param session: the Spark session
    :param file_schema: the schema struct array
    :param input_path: the remote data lake path (s3a://, wasbs://, etc.)
    :return: DataFrame
    """
    logger.info(f"Read JSONL file: {input_path}")

    return (session
            .read
            .json(input_path, multiLine=False)
            )


def to_json(input_df: DataFrame, output_path: str) -> None:
    """
    Read CSV-formatted data and output the results to json.
    """
    logger.info(f"Write to json")

    (input_df
     # .limit(21)
     .write
     .json(path=output_path, mode="overwrite", compression="snappy")
     )


def to_sql(input_df: DataFrame, output_table: str,
           target_jdbc: str) -> None:
    """
    Output the DataFrame to SQL.

    :param input_df: the input DataFrame
    :param output_table: the target SQL table (schema.table)
    :param target_jdbc: sql target (connection string)
    :return: None
    """
    logger.info(f"Write to SQL: {output_table}")

    # Creates a table with given schema
    (input_df
     # .limit(21)
     .withColumn("created_on",
                 to_timestamp(lit(datetime.now()), "yyyyMMdd"))
     .write
     .jdbc(url=target_jdbc,
           table=output_table,
           mode='append')
     )


def to_parquet(input_df: DataFrame, output_path: str) -> None:
    """
    Output the DataFrame to parquet.
    """

    logger.info(f"Write to parquet")

    (input_df
     # .limit(21)
     .write
     .parquet(path=output_path, mode="overwrite")
     )
