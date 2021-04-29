"""
Usage:
- From docker interactive against bitnami docker-compose cluster:
docker run --rm -it --name test_pyspark --network container:spark_ingest_spark_1 spark-ingest:latest /bin/bash
- From Spark 3.1.1 base container with Python bindings:
docker run --rm -it --name test_pyspark spark-ingest:latest /bin/bash
./bin/spark-submit spark-ingest/main.py --filepath ./examples/src/main/python/pi.py
"""
from datetime import datetime, date, timedelta
import logging
import os

# import boto3
import click
from pyspark.sql import SparkSession
# from sqlalchemy import create_engine

import ingest
from ingest.common import (
    psv_to_sql, psv_filter_to_sql
)
from ingest.datasource_config import (
    DS_CONFIG, DS_SUMMARY
)
from ingest.examples import (
    run_mnms, process_schema, FIRE_CONFIG
)

logger = logging.getLogger(__name__)
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARN')


@click.command()
@click.option('--filepath', required=False, help='The input file path')
@click.option('--output_path', required=False, help='The output file path')
def main(filepath: str, output_path: str) -> None:
    """
    To configure AWS bucket-specific authorization, use the
    `fs.s3a.bucket.[bucket name].access.key` configuration setting.

    As specified here:
    - https://hadoop.apache.org/docs/current2/hadoop-aws/tools/hadoop-aws/index.html#Configuring_different_S3_buckets

    TODO: Consider optimizing the S3A for I/O.
    - https://spark.apache.org/docs/3.1.1/cloud-integration.html#recommended-settings-for-writing-to-object-stores
    """
    spark = (SparkSession
             .builder
             .appName("spark_ingest_poc")
             .config(f"fs.s3a.bucket.{os.environ['P3_BUCKET']}.access.key",
                     os.environ['P3_AWS_ACCESS_KEY'])
             .config(f"fs.s3a.bucket.{os.environ['P3_BUCKET']}.secret.key",
                     os.environ['P3_AWS_SECRET_KEY'])
             .config("spark.hadoop.fs.s3a.bucket.bangkok.access.key",
                     os.environ['BK_AWS_ACCESS_KEY'])
             .config("spark.hadoop.fs.s3a.bucket.bangkok.secret.key",
                     os.environ['BK_AWS_SECRET_KEY'])
             .config("spark.hadoop.fs.s3a.bucket.condesa.access.key",
                     os.environ['CO_AWS_ACCESS_KEY'])
             .config("spark.hadoop.fs.s3a.bucket.condesa.secret.key",
                     os.environ['CO_AWS_SECRET_KEY'])
             # TODO: S3A Optimizations
             # .config("spark.hadoop.fs.s3a.committer.name", "directory")
             # .config("spark.sql.sources.commitProtocolClass",
             #         "org.apache.spark.internal.io.cloud.PathOutputCommitProtocol")
             # .config("spark.sql.parquet.output.committer.class",
             #         "org.apache.spark.internal.io.cloud.BindingParquetOutputCommitter")
             # TODO: Parquet Optimizations
             # .config("spark.hadoop.parquet.enable.summary-metadata", "false")
             # .config("spark.sql.parquet.mergeSchema", "false")
             # .config("spark.sql.parquet.filterPushdown", "true")
             # .config("spark.sql.hive.metastorePartitionPruning", "true")
             .getOrCreate()
             )
    spark.sparkContext.setLogLevel(LOG_LEVEL)

    start = datetime.now()
    logger.info(f"Load process started")

    psv_filter_to_sql(spark,
                      filter_date=date.today() - timedelta(days=1),
                      target_jdbc=os.environ['TARGET_JDBC_URL'],
                      **DS_SUMMARY)

    for i, task in enumerate(DS_CONFIG[:], start=1):

        task_name = os.path.split(task['input'])[1]
        logger.info(f"Loading {task_name} ({i} of {len(DS_CONFIG)})")

        psv_to_sql(spark,
                   file_schema=task['schema'],
                   input_path=task['input'],
                   output_table=task['output'],
                   target_jdbc=os.environ['TARGET_JDBC_URL'])

    logger.info(f"Load process finished in {datetime.now() - start}")

    spark.stop()


if __name__ == "__main__":

    main()
