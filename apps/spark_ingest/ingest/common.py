import logging
import os

import ingest

logger = logging.getLogger(__name__)


def psv_to_sql(session, file_schema, input_path: str, output_table: str) -> None:
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

    :param session: the Spark session
    :param file_schema: the schema struct array
    :param input_path: the remote data lake path (s3a://, wasbs://, etc.)
    :param output_table: the target SQL table (schema.table)
    :return: None
    """
    logger.info(f"Read PSV file: {input_path}")

    file_df = (session.
               read.
               csv(input_path, sep='|', header=False, schema=file_schema)
               )

    logger.info(f"Write to SQL: {output_table}")

    (file_df
     .write
     .mode('overwrite')
     .format("jdbc")
     .option("url", os.environ['TARGET_JDBC_URL'])
     .option("dbtable", output_table)
     .option("user", os.environ['TARGET_DB_USER'])
     .option("password", os.environ['TARGET_DB_PASSWORD'])
     .save()
     )


def psv_to_parquet(session, file_schema, input_path: str, output_path: str) -> None:
    """
    Read PSV-formatted data and output the results to parquet.
    """
    logger.info(f"Read PSV file")

    file_df = (session.
               read.
               csv(input_path, sep='|', header=False, schema=file_schema)
               )

    logger.info(f"Write to parquet")

    (file_df.
     write.
     format("parquet").
     mode("overwrite").
     save(output_path)
     )
