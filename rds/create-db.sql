DROP TABLE IF EXISTS public.zipcode_us CASCADE;
DROP TABLE IF EXISTS public.zipcode_ca CASCADE;
DROP TABLE IF EXISTS public.zipcode_mx CASCADE;
DROP TABLE IF EXISTS public.zipcode_gb CASCADE;
DROP TABLE IF EXISTS public.zipcode_es CASCADE;
DROP TABLE IF EXISTS public.zipcode_fr CASCADE;
DROP TABLE IF EXISTS public.zipcode_nz CASCADE;
DROP TABLE IF EXISTS public.zipcode_jp CASCADE;
DROP TABLE IF EXISTS public.zipcode_ph CASCADE;
DROP TABLE IF EXISTS public.zipcode_th CASCADE;

CREATE UNLOGGED TABLE IF NOT EXISTS public.zipcode_us
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

CREATE UNLOGGED TABLE IF NOT EXISTS public.zipcode_ca
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

CREATE UNLOGGED TABLE IF NOT EXISTS public.zipcode_mx
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

CREATE UNLOGGED TABLE IF NOT EXISTS public.zipcode_gb
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

CREATE UNLOGGED TABLE IF NOT EXISTS public.zipcode_es
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

CREATE UNLOGGED TABLE IF NOT EXISTS public.zipcode_fr
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

CREATE UNLOGGED TABLE IF NOT EXISTS public.zipcode_nz
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

CREATE UNLOGGED TABLE IF NOT EXISTS public.zipcode_jp
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

CREATE UNLOGGED TABLE IF NOT EXISTS public.zipcode_ph
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

CREATE UNLOGGED TABLE IF NOT EXISTS public.zipcode_th
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
-- SELECT aws_s3.table_import_from_s3(
--    'public.zipcode',
--    '',
--    '(format text)',
--    aws_commons.create_s3_uri(
--        'condesa',
--        'US.txt',
--        'us-east-2'
--     )
-- );

-- Alternate syntax (requires IAM access)
-- SELECT aws_s3.table_import_from_s3(
--     'public.zipcode',
--     '',
--     '(format text)',
--     'condesa',
--     'US.txt',
--     'us-east-2'
-- );

-- Generated from Redshift UNLOAD
-- SELECT aws_s3.table_import_from_s3(
--     'public.zipcode',
--     '',
--     '(format text)',
--     'bangkok',
--     'us_zipcode0000_part_00',
--     'us-east-2'
-- );

-- TODO: Try COPY FROM syntax