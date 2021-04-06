"""

"""
import logging

from pyspark.sql.functions import (
    col, concat, expr, lit
)
from pyspark.sql.types import (
    StringType, StructType, StructField, IntegerType,
    ArrayType
)

import ingest


logger = logging.getLogger(__name__)


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
