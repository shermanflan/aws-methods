"""
"""
import asyncio
from datetime import datetime
import logging
from operator import add

import boto3
import click
from pyspark.sql import SparkSession
# from sqlalchemy import create_engine

logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s]: %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.INFO)

logger = logging.getLogger(__name__)


@click.command()
@click.option('--filepath', required=True, help='The input file path')
def main(filepath: str) -> None:
    """
    Usage:
    - From docker:
    docker run --rm --name test_pyspark --network container:spark_ingest_spark_1 spark-ingest:latest
    - From docker interactive:
    docker run --rm -it --name test_pyspark --network container:spark_ingest_spark_1 spark-ingest:latest /bin/bash
    """
    spark = (SparkSession
             .builder
             .appName("PythonWordCount")
             .master('spark://spark:7077')
             # .config(f"fs.azure.account.key.{STORAGE_ACCOUNT}.blob.core.windows.net", STORAGE_KEY)
             .getOrCreate()
             )
    lines = spark.read.text(filepath).rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
    output = counts.collect()
    for (word, count) in output:
        print("%s: %i" % (word, count))

    spark.stop()


if __name__ == "__main__":

    main()
