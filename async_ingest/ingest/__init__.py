import asyncio
import logging
from datetime import datetime
import os
import time

from sqlalchemy import text

logger = logging.getLogger(__name__)

redshift_iam = os.environ.get('REDSHIFT_IAM')
UNLOAD_SQL = """
UNLOAD (:sql)
TO :s3_path
iam_role :iam
DELIMITER AS '\t'
MANIFEST ALLOWOVERWRITE
"""


async def load_async(engine):

    await asyncio.gather(
        asyncio.to_thread(
            unloader,
            engine,
            sql='SELECT * FROM public.zipcode_ca',
            s3_path='s3://bangkok/ca_zipcode'),
        asyncio.to_thread(
            unloader,
            engine,
            sql='SELECT * FROM public.zipcode_us',
            s3_path='s3://bangkok/us_zipcode'),
        asyncio.to_thread(
            unloader,
            engine,
            sql='SELECT * FROM public.zipcode_mx',
            s3_path='s3://bangkok/mx_zipcode'),
        asyncio.to_thread(
            unloader,
            engine,
            sql='SELECT * FROM public.zipcode_gb',
            s3_path='s3://bangkok/gb_zipcode'),
    )


def load_sync(engine):

    unloader(engine,
             sql='SELECT * FROM public.zipcode_ca',
             s3_path='s3://bangkok/ca_zipcode')

    unloader(engine,
             sql='SELECT * FROM public.zipcode_us',
             s3_path='s3://bangkok/us_zipcode')

    unloader(engine,
             sql='SELECT * FROM public.zipcode_mx',
             s3_path='s3://bangkok/mx_zipcode')

    unloader(engine,
             sql='SELECT * FROM public.zipcode_gb',
             s3_path='s3://bangkok/gb_zipcode')


def unloader(engine, sql, s3_path):
    start = datetime.now()
    logger.info(f"Processing started at {start}")

    """
    The most basic function of the Engine is to provide access to a Connection, 
    which can then invoke SQL statements.
    """
    with engine.connect() as cnxn:
        cnxn.execute(text(UNLOAD_SQL),
                     sql=sql,
                     s3_path=s3_path,
                     iam=redshift_iam)

    """
    When using an Engine with multiple Python processes, such as when using
    os.fork or Python multiprocessing, it’s important that the engine is 
    initialized per process. 

    TODO: See Using Connection Pools with Multiprocessing or os.fork() for 
    details.
    """

    # TODO: Compare performance with session API
    # https://docs.sqlalchemy.org/en/13/orm/session_basics.html
    # time.sleep(2)

    logger.info(f"Processing completed after {datetime.now() - start}")
