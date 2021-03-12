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


def test_algo(s: str) -> int:
    memo = [[0]*len(s) for _ in range(len(s))]
    max_len = 0

    for d in range(len(s)):
        memo[d][d] = 1

    col = 1
    while col < len(s):

        row = 0
        while row + col < len(s):

            if s[row] == s[row + col] and col == 1:
                memo[row][row + col] = 2
            elif s[row] == s[row + col]:
                memo[row][row + col] = memo[row + 1][row + col - 1] + 2
            else:
                memo[row][row + col] = max(memo[row][row + col - 1], memo[row + 1][row + col])

            max_len = max(max_len, memo[row][row + col])
            row += 1
        col += 1

    print(memo)
    return max_len


def main():

    start = datetime.now()

    acquire_sync(rs_engine, pg_engine)

    logger.info(f"Total sync elapsed: {datetime.now() - start}")

    start = datetime.now()

    asyncio.run(acquire_async(rs_engine, pg_engine))

    logger.info(f"Total async elapsed: {datetime.now() - start}")


if __name__ == "__main__":

    main()
    # print(test_algo('LPASPAL'))
