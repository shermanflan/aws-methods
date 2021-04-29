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

# import boto3
import click
from pyspark.sql import SparkSession
# from sqlalchemy import create_engine

import ingest
from ingest.datasource_config import DS_CONFIG
from ingest.common import (
    psv_to_sql
)
# from ingest.examples import (
#     run_mnms, process_schema, process_large_csv
# )

logger = logging.getLogger(__name__)
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARN')


@click.command()
@click.option('--filepath', required=False, help='The input file path')
@click.option('--output_path', required=False, help='The output file path')
def main(filepath: str, output_path: str) -> None:
    spark = (SparkSession
             .builder
             .appName("spark_ingest_poc")
             # TODO: Configure different buckets
             # https://hadoop.apache.org/docs/current2/hadoop-aws/tools/hadoop-aws/index.html#Configuring_different_S3_buckets
             # .config(f"fs.s3a.bucket.[bucket_name].access.key", AWS_ACCESS_KEY)
             # .config(f"fs.s3a.bucket.[bucket_name].secret.key", AWS_SECRET_KEY)
             .getOrCreate()
             )
    spark.sparkContext.setLogLevel(LOG_LEVEL)

    start = datetime.now()
    logger.info(f"Load process started")

    for i, task in enumerate(DS_CONFIG[:], start=1):

        task_name = os.path.split(task['input'])[1]
        logger.info(f"Loading {task_name} ({i} of {len(DS_CONFIG)})")

        psv_to_sql(spark,
                   file_schema=task['schema'],
                   input_path=task['input'],
                   output_table=task['output'])

    logger.info(f"Load process finished in {datetime.now() - start}")

    spark.stop()


if __name__ == "__main__":

    main()

    # Examples
    # run_mnms(spark, filepath)
    # process_large_csv(spark, filepath, output_path)
