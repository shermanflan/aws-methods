import asyncio
from datetime import datetime
from itertools import starmap
import logging
import os
from urllib.parse import urlparse

from sqlalchemy import text

from ingest import (
    UNLOAD_SQL, LOAD_SQL, IAM_REDSHIFT,
    ETL_MAPPING
)

logger = logging.getLogger(__name__)


async def acquire_async(source, target, lake) -> None:
    """
    Seems superior to async unload => sync load:

    tasks = (
        asyncio.to_thread(_acquire, source, target, lake, **config)
        for config in ETL_MAPPING[:2]
    )

    :param source:
    :param target:
    :param lake:
    :return:
    """
    tasks = starmap(_acquire_async, [(source, target, lake, *config.values())
                                     for config in ETL_MAPPING[:]])

    await asyncio.gather(*tasks)


async def _acquire_async(source, target, lake, table: str, sql: str,
                         lake_path: str) -> None:

    await asyncio.gather(
        asyncio.to_thread(unloader, source, sql, lake_path)
    )

    logger.info(f"Searching prefixes for {lake_path}")

    parts = urlparse(lake_path)
    exports = lake.list_objects_v2(Bucket=parts.hostname,
                                   Prefix=parts.path[1:])

    load_tasks = (
        asyncio.to_thread(loader, target, table, parts.hostname, part['Key'])
        for part in exports.get('Contents', [])
        if not part['Key'].endswith('manifest') and part['Size'] > 0
    )

    await asyncio.gather(*load_tasks)


def acquire_sync(source, target, lake) -> None:

    for table_config in ETL_MAPPING[:]:
        _acquire_sync(source, target, lake, **table_config)


def _acquire_sync(source, target, lake, table: str, sql: str, lake_path: str) -> None:

    unloader(source, sql, lake_path)

    logger.info(f"Searching prefixes for {lake_path}")

    s3_parts = urlparse(lake_path)
    exports = lake.list_objects_v2(
        Bucket=s3_parts.hostname,
        Prefix=s3_parts.path[1:]
    )

    for part in exports.get('Contents', []):
        if part['Key'].endswith('manifest') or part['Size'] == 0:
            continue

        logger.info(f"Loading from s3 Path: {part['Key']}")

        loader(target,
               table,
               bucket=s3_parts.hostname,
               lake_path=part['Key']
               )


def unloader(db, sql: str, lake_path: str) -> None:
    """
    Try to do the majority of processing at the source. If views cannot be
    created, then issue joined SQL.

    The most basic function of the Engine is to provide access to a Connection,
    which can then invoke SQL statements.

    When using an Engine with multiple Python processes, such as when using
    os.fork or Python multiprocessing, it’s important that the engine is
    initialized per process.

    TODO:
    - See Using Connection Pools with Multiprocessing or os.fork() for details.
    - Compare performance with session API
    https://docs.sqlalchemy.org/en/13/orm/session_basics.html
    - Add tenacity retries

    :param db:
    :param sql:
    :param lake_path:
    :return:
    """
    start = datetime.now()
    logger.info(f"Unloader started at {start} for {os.path.split(lake_path)[1]}")

    with db.connect() as con:
        con.execute(text(UNLOAD_SQL), sql=sql, lake_path=lake_path,
                    iam=IAM_REDSHIFT)

    logger.info("Unloader completed after {0} for {1}".format(
        datetime.now() - start,
        os.path.split(lake_path)[1]
    ))


def loader(db, table: str, bucket: str, lake_path: str) -> None:
    """
    TODO:
    - Add tenacity retries

    :param db:
    :param table:
    :param bucket:
    :param lake_path:
    :return:
    """
    start = datetime.now()
    logger.info(f"Loader for {table} started at {start}")

    with db.connect().execution_options(autocommit=True) as con:
        con.execute(text(LOAD_SQL), table=table, bucket=bucket,
                    path=lake_path)

    logger.info(f"Loader for {table} completed after {datetime.now() - start}")
