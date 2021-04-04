"""
"""
import asyncio
from datetime import datetime
import logging
from operator import add
import os

import boto3
import click
from pyspark.sql import SparkSession
# from sqlalchemy import create_engine

logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s]: %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.INFO)

logger = logging.getLogger(__name__)
STORAGE_ACCOUNT=os.environ.get('AZ_STORAGE_ACCOUNT_NAME')
STORAGE_KEY=os.environ.get('AZ_STORAGE_ACCOUNT_KEY')


@click.command()
@click.option('--filepath', required=True, help='The input file path')
def main(filepath: str) -> None:
    """
    Usage:
    - From docker interactive against bitnami docker-compose cluster:
    docker run --rm -it --name test_pyspark --network container:spark_ingest_spark_1 spark-ingest:latest /bin/bash
    - From Spark 3.1.1 base container with Python bindings:
    docker run --rm -it --name test_pyspark spark-ingest:latest /bin/bash
    ./bin/spark-submit spark-ingest/main.py --filepath ./examples/src/main/python/pi.py
    """
    logger.info(f"M&Ms process started")
    logger.info(f"M&Ms process using credentials from {STORAGE_ACCOUNT} with {STORAGE_KEY}")

    spark = (SparkSession
             .builder
             .appName("PythonMnMCount")
             # .master('spark://spark:7077')
             .config(f"fs.azure.account.key.{STORAGE_ACCOUNT}.blob.core.windows.net", STORAGE_KEY)
             .getOrCreate()
             )

    logger.info(f"Reading M&Ms file: [{filepath}]")

    file_df = (spark.
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

    spark.stop()


if __name__ == "__main__":

    main()
