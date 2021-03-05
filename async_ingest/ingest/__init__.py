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

LOAD_SQL = """
SELECT aws_s3.table_import_from_s3(
    :table,
    '',
    '(format text)',
    :bucket,
    :path,
    'us-east-2'
)
"""


async def acquire_async(source_engine, target_engine):

    await asyncio.gather(
        asyncio.to_thread(
            acquire_1,
            source_engine,
            target_engine,
        ),
        asyncio.to_thread(
            acquire_2,
            source_engine,
            target_engine,
        ),
        asyncio.to_thread(
            acquire_3,
            source_engine,
            target_engine,
        ),
        asyncio.to_thread(
            acquire_4,
            source_engine,
            target_engine,
        )
    )


def acquire_sync(source_engine, target_engine):
    acquire_1(source_engine, target_engine)
    acquire_2(source_engine, target_engine)
    acquire_3(source_engine, target_engine)
    acquire_4(source_engine, target_engine)


def acquire_1(source_engine, target_engine):
    # TODO: Make sql and s3_path data driven (YAML, table, etc.)
    unloader(source_engine,
             sql='SELECT * FROM public.zipcode_us',
             s3_path='s3://bangkok/us_zipcode')

    # TODO: Get all prefixes for s3://bangkok/us_zipcode/YYYY/MM/DD
    # TODO: Consider another asyncio.gather for the loads
    loader(target_engine,
           table='public.zipcode_us',
           bucket='bangkok',
           s3_path='us_zipcode0000_part_00'
           )

    # TODO: Make table and s3_path data driven (YAML, table, etc.)
    loader(target_engine,
           table='public.zipcode_us',
           bucket='bangkok',
           s3_path='us_zipcode0001_part_00'
           )


def acquire_2(source_engine, target_engine):

    unloader(source_engine,
             sql='SELECT * FROM public.zipcode_ca',
             s3_path='s3://bangkok/ca_zipcode')

    loader(target_engine,
           table='public.zipcode_ca',
           bucket='bangkok',
           s3_path='ca_zipcode0000_part_00'
           )


def acquire_3(source_engine, target_engine):

    unloader(source_engine,
             sql='SELECT * FROM public.zipcode_mx',
             s3_path='s3://bangkok/mx_zipcode')

    loader(target_engine,
           table='public.zipcode_mx',
           bucket='bangkok',
           s3_path='mx_zipcode0000_part_00'
           )

    loader(target_engine,
           table='public.zipcode_us',
           bucket='bangkok',
           s3_path='mx_zipcode0001_part_00'
           )


def acquire_4(source_engine, target_engine):

    unloader(source_engine,
             sql='SELECT * FROM public.zipcode_gb',
             s3_path='s3://bangkok/gb_zipcode')

    loader(target_engine,
           table='public.zipcode_gb',
           bucket='bangkok',
           s3_path='gb_zipcode0000_part_00'
           )

    loader(target_engine,
           table='public.zipcode_gb',
           bucket='bangkok',
           s3_path='gb_zipcode0001_part_00'
           )


def unloader(engine, sql, s3_path):
    start = datetime.now()
    logger.info(f"Unloader started at {start}")

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

    logger.info(f"Unloader completed after {datetime.now() - start}")


def loader(engine, table, bucket, s3_path):
    start = datetime.now()
    logger.info(f"Loader started at {start}")

    with engine.connect().execution_options(autocommit=True) as cnxn:
        cnxn.execute(f"TRUNCATE TABLE {table}")

        # TODO: parse 's3://bangkok/ca_zipcode' using rex
        cnxn.execute(text(LOAD_SQL),
                     table=table,
                     bucket=bucket,
                     path=s3_path
                     )

    logger.info(f"Loader completed after {datetime.now() - start}")
