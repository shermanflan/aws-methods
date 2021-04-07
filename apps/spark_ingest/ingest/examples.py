"""

"""
import logging

from pyspark.sql.functions import (
    col, concat, expr, lit, sum as spark_sum, to_timestamp,
    year as spark_year
)
from pyspark.sql.types import (
    StringType, StructType, StructField, IntegerType,
    ArrayType, BooleanType, FloatType
)

import ingest


logger = logging.getLogger(__name__)


def process_large_csv(session, input_path: str, output_path: str) -> None:
    """
    Read a large CSV and output the aggregated results to parquet.
    """
    # Programmatic way to define a schema
    fire_schema = StructType([
        StructField('CallNumber', IntegerType(), True),
        StructField('UnitID', StringType(), True),
        StructField('IncidentNumber', IntegerType(), True),
        StructField('CallType', StringType(), True),
        StructField('CallDate', StringType(), True),
        StructField('WatchDate', StringType(), True),
        StructField('CallFinalDisposition', StringType(), True),
        StructField('AvailableDtTm', StringType(), True),
        StructField('Address', StringType(), True),
        StructField('City', StringType(), True),
        StructField('Zipcode', IntegerType(), True),
        StructField('Battalion', StringType(), True),
        StructField('StationArea', StringType(), True),
        StructField('Box', StringType(), True),
        StructField('OriginalPriority', StringType(), True),
        StructField('Priority', StringType(), True),
        StructField('FinalPriority', IntegerType(), True),
        StructField('ALSUnit', BooleanType(), True),
        StructField('CallTypeGroup', StringType(), True),
        StructField('NumAlarms', IntegerType(), True),
        StructField('UnitType', StringType(), True),
        StructField('UnitSequenceInCallDispatch', IntegerType(), True),
        StructField('FirePreventionDistrict', StringType(), True),
        StructField('SupervisorDistrict', StringType(), True),
        StructField('Neighborhood', StringType(), True),
        StructField('Location', StringType(), True),
        StructField('RowID', StringType(), True),
        StructField('Delay', FloatType(), True)]
    )

    # Use the DataFrameReader interface to read a CSV file
    fire_df = (session.
               read.
               csv(input_path, header=True, schema=fire_schema)
               )

    counts = (fire_df.
              withColumn("CallYear", to_timestamp(col("CallDate"), "MM/dd/yyyy")).
              withColumnRenamed("NumAlarms", "Alarms").
              where((col("CallType") != "Medical Incident") & col("CallDate").isNotNull()).
              select('City', spark_year('CallYear').alias('Year'), 'CallType', 'Alarms').
              groupBy('City', 'Year', 'CallType').
              agg(spark_sum('Alarms').alias("TotalAlarms")).
              orderBy("TotalAlarms", ascending=False)
              )

    counts.show(n=21, truncate=False)

    # Save as parquet
    (counts.
     write.
     format("parquet").
     save(output_path))


def process_schema(session, filepath: str) -> None:
    """
    Reads a JSON formatted file from a remote data lake and applies an
    explicitly-defined data schema.

    Tips:
    - Always define your schema up front whenever you want to read a large
      file from a data source
    """
    # Define data schema
    # schema = StructType([
    #     StructField("Id", IntegerType(), False),
    #     StructField("First", StringType(), False),
    #     StructField("Last", StringType(), False),
    #     StructField("Url", StringType(), False),
    #     StructField("Published", StringType(), False),
    #     StructField("Hits", IntegerType(), False),
    #     StructField("Campaigns", ArrayType(StringType()), False)]
    # )
    # Using declarative syntax
    schema = """
        `Id` INT, 
        `First` STRING, 
        `Last` STRING, 
        `Url` STRING,
        `Published` STRING, 
        `Hits` INT, 
        `Campaigns` ARRAY < STRING >
    """

    # Create data manually
    # data = [[1, "Jules", "Damji", "https://tinyurl.1", "1/4/2016", 4535, ["twitter", "LinkedIn"]],
    #         [2, "Brooke", "Wenig", "https://tinyurl.2", "5/5/2018", 8908, ["twitter", "LinkedIn"]],
    #         [3, "Denny", "Lee", "https://tinyurl.3", "6/7/2019", 7659, ["web", "twitter", "FB", "LinkedIn"]],
    #         [4, "Tathagata", "Das", "https://tinyurl.4", "5/12/2018", 10568, ["twitter", "FB"]],
    #         [5, "Matei", "Zaharia", "https://tinyurl.5", "5/14/2014", 40578, ["web", "twitter", "FB", "LinkedIn"]],
    #         [6, "Reynold", "Xin", "https://tinyurl.6", "3/2/2015", 25568, ["twitter", "LinkedIn"]]
    #         ]

    # create a DataFrame using the schema defined above
    # blogs_df = session.createDataFrame(data, schema)

    # Read from remote data lake
    blogs_df = (session.
                read.
                schema(schema).
                json(filepath)
                )

    # show the DataFrame; it should reflect our table above
    blogs_df.show()

    # print the schema used by Spark to process the DataFrame
    logger.info(blogs_df.printSchema())

    # Show columns and expressions
    blogs_df.select(expr("Hits") * 2).show(2)
    blogs_df.select(col("Hits") * 2).show(2)
    blogs_df.select(expr("Hits * 2")).show(2)

    # show heavy hitters
    (blogs_df.
     withColumn("Full Name", (concat(col("Last"), lit(', '), expr("First")))).
     withColumn("Big Hitters", (expr("Hits > 10000"))).
     sort(col("Hits").desc()).
     show()
     )

    logger.info(blogs_df.schema)


def run_mnms(session, filepath: str) -> None:
    """
    Simple example which reads a CSV file from a cloud data lake
    and performs a set of aggregations on the data.

    :param session: the Spark session
    :param filepath: the remote data lake path (s3a://, wasbs://, etc.)
    :return: None
    """
    logger.info(f"Reading M&Ms file: [{filepath}]")

    file_df = (session.
               read.
               format('csv').
               option('header', 'true').
               option('inferSchema', 'true').
               load(filepath)
               )

    counts = (file_df.
              select('State', 'Color', 'Count').
              groupBy('State', 'Color').
              sum('Count').
              orderBy("sum(Count)", ascending=False)
              )

    logger.info(f"M&Ms agg 1")

    counts.show(n=60, truncate=False)

    logger.info(f"M&Ms! {counts.count()}")

    counts_ca = (file_df.
                 select('State', 'Color', 'Count').
                 where(file_df.State == 'CA').
                 groupBy('State', 'Color').
                 sum('Count').
                 orderBy("sum(Count)", ascending=False)
                 )

    logger.info(f"M&Ms agg 2")

    counts_ca.show(n=10, truncate=False)
