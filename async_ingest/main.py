import asyncio
from datetime import datetime
import logging

import boto3
import click
from sqlalchemy import create_engine

from ingest import REDSHIFT_DB_URL, POSTGRES_DB_URL
from ingest.etl import acquire_sync, acquire_async

logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s]: %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.INFO)

logger = logging.getLogger(__name__)

"""
The typical usage of create_engine() is once per particular database URL, 
held globally for the lifetime of a single application process. A single 
Engine manages many individual DBAPI connections on behalf of the process 
and is intended to be called upon in a concurrent fashion. The Engine is 
most efficient when created just once at the module level of an application, 
not per-object or per-function call. 
"""


def test_algo(s1: str, s2: str) -> int:
    memo = [[0]*(len(s2) + 1) for _ in range(len(s1) + 1)]
    max_len = 0
    breadcrumbs = {}

    for row in range(1, len(s1) + 1):
        for col in range(len(s2) + 1):
            if s1[row-1] == s2[col-1]:
                memo[row][col] = 1 + memo[row-1][col-1]
                if memo[row][col] > max_len:
                    max_len = memo[row][col]
                    breadcrumbs[(row, col)] = (row-1, col-1)
    return max_len, breadcrumbs, memo


@click.command()
@click.option('--asynchronous/--no-asynchronous', default=True,
              show_default=True, help='Set/unset asynchronous behavior')
def main(asynchronous: bool) -> None:
    """
    Run extract from Redshift and load to postgresql using bulk import/export
    features.
    """
    rs_engine = create_engine(REDSHIFT_DB_URL, echo=False)
    pg_engine = create_engine(POSTGRES_DB_URL, echo=False)
    s3_client = boto3.client('s3')

    if asynchronous:
        start = datetime.now()

        asyncio.run(acquire_async(rs_engine, pg_engine, s3_client))

        logger.info(f"Total async elapsed: {datetime.now() - start}")
    else:
        start = datetime.now()

        acquire_sync(rs_engine, pg_engine, s3_client)

        logger.info(f"Total sync elapsed: {datetime.now() - start}")


if __name__ == "__main__":

    main()
    # print(test_algo('XLCabb', 'YabbaX'))
