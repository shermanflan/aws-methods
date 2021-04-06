"""
Usage:
- From docker interactive against bitnami docker-compose cluster:
docker run --rm -it --name test_pyspark --network container:spark_ingest_spark_1 spark-ingest:latest /bin/bash
- From Spark 3.1.1 base container with Python bindings:
docker run --rm -it --name test_pyspark spark-ingest:latest /bin/bash
./bin/spark-submit spark-ingest/main.py --filepath ./examples/src/main/python/pi.py
"""
from datetime import datetime
import logging
import os

import boto3
import click
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg
# from sqlalchemy import create_engine

import ingest
from ingest.examples import (
    run_mnms, process_schema
)

logger = logging.getLogger(__name__)
STORAGE_ACCOUNT = os.environ.get('AZ_STORAGE_ACCOUNT_NAME')
STORAGE_KEY = os.environ.get('AZ_STORAGE_ACCOUNT_KEY')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARN')

@click.command()
@click.option('--filepath', required=True, help='The input file path')
def main(filepath: str) -> None:
    spark = (SparkSession
             .builder
             .appName("spark_ingest_poc")
             .config(f"fs.azure.account.key.{STORAGE_ACCOUNT}.blob.core.windows.net", STORAGE_KEY)
             .getOrCreate()
             )
    spark.sparkContext.setLogLevel(LOG_LEVEL)

    # logger.info(f"M&Ms process started")
    # run_mnms(spark, filepath)

    # Scratch
    process_schema(spark, filepath)

    spark.stop()


if __name__ == "__main__":

    main()
