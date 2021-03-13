import asyncio
import collections
from datetime import datetime
import logging
import os
import time

import boto3
from sqlalchemy import create_engine

from ingest.etl import acquire_sync, acquire_async

logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s]: %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.INFO)

logger = logging.getLogger(__name__)
redshift_db_url = os.environ.get('REDSHIFT_DB_URL')
postgres_db_url = os.environ.get('POSTGRES_DB_URL')

"""
The typical usage of create_engine() is once per particular database URL, 
held globally for the lifetime of a single application process. A single 
Engine manages many individual DBAPI connections on behalf of the process 
and is intended to be called upon in a concurrent fashion. The Engine is 
most efficient when created just once at the module level of an application, 
not per-object or per-function call. 
"""
rs_engine = create_engine(redshift_db_url, echo=False)
pg_engine = create_engine(postgres_db_url, echo=False)
s3_client = boto3.client('s3')


def test_algo(arr: [int]) -> int:
    memo = [[n] for n in arr]
    max_len, max_index = 1, 0

    for i in range(1, len(arr)):
        if arr[i] > memo[i-1][-1]:
            memo[i] = memo[i-1].copy()
            memo[i].append(arr[i])
        else:
            prev = i - 2
            while prev >= 0 and arr[i] <= memo[prev][-1]:
                prev -= 1

            if prev >= 0:
                memo[i] = memo[prev].copy()
                memo[i].append(arr[i])

        if len(memo[i]) > max_len:
            max_index = i

    print(memo)
    return memo[max_index]


def main():

    start = datetime.now()

    acquire_sync(rs_engine, pg_engine, s3_client)

    logger.info(f"Total sync elapsed: {datetime.now() - start}")

    start = datetime.now()

    asyncio.run(acquire_async(rs_engine, pg_engine, s3_client))

    logger.info(f"Total async elapsed: {datetime.now() - start}")


if __name__ == "__main__":

    # s3 = boto3.resource('s3')
    # for bucket in s3.buckets.all():
    #     logger.info(bucket.name)

    # s3_client = boto3.client('s3')
    # buckets = s3_client.list_buckets()['Buckets']
    # for bucket in buckets:
    #     logger.info(f"Listing objects in {bucket['Name']}")
    #
    #     exports = s3_client.list_objects_v2(
    #         Bucket=bucket['Name'],
    #         Prefix='th'
    #     )
    #
    #     for part in exports.get('Contents', []):
    #         logger.info(f"{part['Key']}")

    main()
    # print(test_algo([3, 1, 5, 2, 6, 4, 9]))
