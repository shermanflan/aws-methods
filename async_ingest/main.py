import logging
import os

from sqlalchemy import create_engine

logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s]: %(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    redshift_db_url = os.environ.get('REDSHIFT_DB_URL')
    """
    The typical usage of create_engine() is once per particular database URL, 
    held globally for the lifetime of a single application process. A single 
    Engine manages many individual DBAPI connections on behalf of the process 
    and is intended to be called upon in a concurrent fashion. The Engine is 
    not synonymous to the DBAPI connect function, which represents just one 
    connection resource - the Engine is most efficient when created just once 
    at the module level of an application, not per-object or per-function call. 
    """
    engine = create_engine(redshift_db_url)

    """
    The most basic function of the Engine is to provide access to a Connection, 
    which can then invoke SQL statements. To emit a textual statement to the 
    database looks like:
    """
    with engine.connect() as cnxn:
        result = cnxn.execute("select COUNT(*) AS total from public.zipcode_gb")
        for row in result:
            logger.info(f"Total: {row['total']}")

    """
    When using an Engine with multiple Python processes, such as when using
    os.fork or Python multiprocessing, it’s important that the engine is 
    initialized per process. 
    
    TODO: See Using Connection Pools with Multiprocessing or os.fork() for 
    details.
    """

    # TODO: Compare performance with session API
    # https://docs.sqlalchemy.org/en/13/orm/session_basics.html

    logger.info("Processing complete")
