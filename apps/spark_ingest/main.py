"""
Usage:
- From docker interactive against bitnami docker-compose cluster:
docker run --rm -it --name test_pyspark --network container:spark_ingest_spark_1 spark-ingest:latest /bin/bash
- From Spark 3.1.1 base container with Python bindings:
docker run --rm -it --name test_pyspark spark-ingest:latest /bin/bash
./bin/spark-submit spark-ingest/main.py --filepath ./examples/src/main/python/pi.py
"""
import logging
import os

# import boto3
import click
from pyspark.sql import SparkSession
# from sqlalchemy import create_engine

import ingest
from ingest.healthjump_config import HJ_META
from ingest.common import (
    psv_to_sql
)
# from ingest.examples import (
#     run_mnms, process_schema, process_large_csv
# )

logger = logging.getLogger(__name__)
# STORAGE_ACCOUNT = os.environ.get('AZ_STORAGE_ACCOUNT_NAME')
# STORAGE_KEY = os.environ.get('AZ_STORAGE_ACCOUNT_KEY')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARN')


@click.command()
@click.option('--filepath', required=True, help='The input file path')
@click.option('--output_path', required=False, help='The output file path')
def main(filepath: str, output_path: str) -> None:
    spark = (SparkSession
             .builder
             .appName("spark_ingest_poc")
             # .config(f"fs.azure.account.key.{STORAGE_ACCOUNT}.blob.core.windows.net",
             #         STORAGE_KEY)
             .getOrCreate()
             )
    spark.sparkContext.setLogLevel(LOG_LEVEL)

    # Examples
    # run_mnms(spark, filepath)
    # process_large_csv(spark, filepath, output_path)

    logger.info(f"Load process started")

    for task in HJ_META[:]:
        psv_to_sql(spark,
                   file_schema=task['schema'],
                   input_path=task['input'],
                   output_table=task['output'])

    logger.info(f"Load process finished")

    spark.stop()


if __name__ == "__main__":

    main()
