import asyncio
from datetime import datetime
import logging
import os
import time

from sqlalchemy import create_engine

from ingest import unload_sync, unload_async

logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s]: %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.DEBUG)

logger = logging.getLogger(__name__)
redshift_db_url = os.environ.get('REDSHIFT_DB_URL')

"""
The typical usage of create_engine() is once per particular database URL, 
held globally for the lifetime of a single application process. A single 
Engine manages many individual DBAPI connections on behalf of the process 
and is intended to be called upon in a concurrent fashion. The Engine is 
most efficient when created just once at the module level of an application, 
not per-object or per-function call. 
"""
engine = create_engine(redshift_db_url)


def test_algo(nums, memo):

    if len(nums) in (0, 1):
        return 1

    result = 0

    for i in range(len(nums)):
        if len(nums[:i]) in memo:
            left = memo[len(nums[:i])]
        else:
            memo[len(nums[:i])] = test_algo(nums[:i], memo)
            left = memo[len(nums[:i])]

        if i < (len(nums) - 1) and len(nums[i+1:]) in memo:
            right = memo[len(nums[i+1:])]
        elif i < (len(nums) - 1):
            memo[len(nums[i+1:])] = test_algo(nums[i+1:], memo)
            right = memo[len(nums[i+1:])]
        else:
            right = 1

        result += left*right

    return result


def main():

    start = datetime.now()

    unload_sync(engine)

    logger.info(f"Total sync elapsed: {datetime.now() - start}")

    start = datetime.now()

    asyncio.run(unload_async(engine))

    logger.info(f"Total async elapsed: {datetime.now() - start}")


if __name__ == "__main__":

    main()
