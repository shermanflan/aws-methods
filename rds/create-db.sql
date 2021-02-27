DROP TABLE IF EXISTS public.zipcode CASCADE;

CREATE TABLE IF NOT EXISTS public.zipcode
(
    country_code    VARCHAR(2)      NULL,
    postal_code     VARCHAR(20)     NULL,
    place_name      varchar(180)    NULL,
    admin_name1     varchar(100)    NULL,
    admin_code1     varchar(20)     NULL,
    admin_name2     varchar(100)    NULL,
    admin_code2     varchar(20)     NULL,
    admin_name3     varchar(100)    NULL,
    admin_code3     varchar(20)     NULL,
    latitude        REAL            NULL,
    longitude       REAL            NULL,
    accuracy        CHAR(1)         NULL
);

-- Import from S3 using TSV
-- Reference: 
-- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Procedural.Importing.html#USER_PostgreSQL.S3Import
SELECT aws_s3.table_import_from_s3(
   'public.zipcode',
   '',
   '(format text)',
   aws_commons.create_s3_uri(
       'condesa',
       'US.txt',
       'us-east-2'
    )
);

-- Alternate syntax (requires IAM access)
SELECT aws_s3.table_import_from_s3(
    'public.zipcode',
    '',
    '(format text)',
    'condesa',
    'US.txt',
    'us-east-2'
);


select  COUNT(*)
from    public.zipcode
;
