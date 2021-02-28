DROP TABLE IF EXISTS public.zipcode_us CASCADE;

CREATE TABLE IF NOT EXISTS public.zipcode_us
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

DROP TABLE IF EXISTS public.zipcode_ca CASCADE;

CREATE TABLE IF NOT EXISTS public.zipcode_ca
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

-- LOAD from S3
COPY public.zipcode_us
FROM 's3://condesa/US.txt'
iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
DELIMITER AS '\t'
;

COPY public.zipcode_ca
FROM 's3://condesa/CA.txt'
iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
DELIMITER AS '\t'
;

-- UNLOAD to S3
UNLOAD ('SELECT * FROM public.zipcode_us')
TO 's3://bangkok/us_zipcode'
iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
DELIMITER AS '\t'
MANIFEST ALLOWOVERWRITE
;

UNLOAD ('SELECT * FROM public.zipcode_ca')
TO 's3://bangkok/ca_zipcode'
iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
DELIMITER AS '\t'
MANIFEST ALLOWOVERWRITE
;