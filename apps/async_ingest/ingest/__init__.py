from datetime import date
import os

IAM_REDSHIFT = os.environ.get('IAM_REDSHIFT')
REDSHIFT_DB_URL = os.environ.get('REDSHIFT_DB_URL')
POSTGRES_DB_URL = os.environ.get('POSTGRES_DB_URL')

UNLOAD_SQL = """
UNLOAD (:sql)
TO :lake_path
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

_date_path = date.today().strftime('%Y/%m/%d')

ETL_MAPPING = [
    {
        'table': 'public.zipcode_us',
        'sql': 'SELECT * FROM public.zipcode_us',
        'lake_path': f"s3://bangkok/zipcode_us/{_date_path}/us_"
    },
    {
        'table': 'public.zipcode_ca',
        'sql': 'SELECT * FROM public.zipcode_ca',
        'lake_path': f"s3://bangkok/zipcode_ca/{_date_path}/ca_"
    },
    {
        'table': 'public.zipcode_mx',
        'sql': 'SELECT * FROM public.zipcode_mx',
        'lake_path': f"s3://bangkok/zipcode_mx/{_date_path}/mx_"
    },
    {
        'table': 'public.zipcode_gb',
        'sql': 'SELECT * FROM public.zipcode_gb',
        'lake_path': f"s3://bangkok/zipcode_gb/{_date_path}/gb_"
    },
    {
        'table': 'public.zipcode_es',
        'sql': 'SELECT * FROM public.zipcode_es',
        'lake_path': f"s3://bangkok/zipcode_es/{_date_path}/es_"
    },
    {
        'table': 'public.zipcode_fr',
        'sql': 'SELECT * FROM public.zipcode_fr',
        'lake_path': f"s3://bangkok/zipcode_fr/{_date_path}/fr_"
    },
    {
        'table': 'public.zipcode_nz',
        'sql': 'SELECT * FROM public.zipcode_nz',
        'lake_path': f"s3://bangkok/zipcode_nz/{_date_path}/nz_"
    },
    {
        'table': 'public.zipcode_jp',
        'sql': 'SELECT * FROM public.zipcode_jp',
        'lake_path': f"s3://bangkok/zipcode_jp/{_date_path}/jp_"
    },
    {
        'table': 'public.zipcode_ph',
        'sql': 'SELECT * FROM public.zipcode_ph',
        'lake_path': f"s3://bangkok/zipcode_ph/{_date_path}/ph_"
    },
    {
        'table': 'public.zipcode_th',
        'sql': 'SELECT * FROM public.zipcode_th',
        'lake_path': f"s3://bangkok/zipcode_th/{_date_path}/th_"
    },
]
