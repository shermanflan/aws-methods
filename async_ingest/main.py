import asyncio
import collections
from datetime import datetime
import logging
import os
import time

from sqlalchemy import create_engine

from ingest import acquire_sync, acquire_async

logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s]: %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.DEBUG)

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


def test_algo(nums, target):

    memo = [[False]*(target + 1) for _ in range(len(nums) + 1)]
    memo[0][0] = True

    for i, num in enumerate(nums, 1):
        for psum in range(target + 1):
            if memo[i - 1][psum]:
                memo[i][psum] = True
            elif psum - num >= 0 and memo[i - 1][psum - num]:
                memo[i][psum] = True

    return memo[-1][-1]


def main():

    start = datetime.now()

    acquire_sync(rs_engine, pg_engine)

    logger.info(f"Total sync elapsed: {datetime.now() - start}")

    start = datetime.now()

    asyncio.run(acquire_async(rs_engine, pg_engine))

    logger.info(f"Total async elapsed: {datetime.now() - start}")


if __name__ == "__main__":

    main()
    # print(test_algo([1, 3, 9, 2], 16))