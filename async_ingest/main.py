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
    memo = [[0]*(len(s2)+1) for _ in range(len(s1)+1)]
    max_str = ''
    max_len = 0

    for i1 in range(1, len(s1) + 1):
        for i2 in range(1, len(s2) + 1):
            if s1[i1 - 1] == s2[i2 - 1]:
                memo[i1][i2] = 1 + max(memo[i1 - 1][i2 - 1],
                                       memo[i1][i2 - 1],
                                       memo[i1 - 1][i2])
            else:
                memo[i1][i2] = max(memo[i1 - 1][i2 - 1],
                                   memo[i1][i2 - 1],
                                   memo[i1 - 1][i2])

            if memo[i1][i2] > max_len:
                max_len = memo[i1][i2]
                max_str = s1[i1:i2+1]

    return max_len, max_str


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
    # print(test_algo('ACBEA', 'ADCA'))
