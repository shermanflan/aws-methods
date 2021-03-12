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

CREATE TABLE IF NOT EXISTS public.zipcode_mx
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

CREATE TABLE IF NOT EXISTS public.zipcode_gb
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

CREATE TABLE IF NOT EXISTS public.zipcode_es
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

CREATE TABLE IF NOT EXISTS public.zipcode_fr
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

CREATE TABLE IF NOT EXISTS public.zipcode_nz
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

CREATE TABLE IF NOT EXISTS public.zipcode_jp
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

CREATE TABLE IF NOT EXISTS public.zipcode_ph
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

CREATE TABLE IF NOT EXISTS public.zipcode_th
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

COPY public.zipcode_mx
FROM 's3://condesa/MX.txt'
iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
DELIMITER AS '\t'
;

COPY public.zipcode_gb
FROM 's3://condesa/GB.txt'
iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
DELIMITER AS '\t'
;
COPY public.zipcode_es
FROM 's3://condesa/ES.txt'
iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
DELIMITER AS '\t'
;

COPY public.zipcode_fr
FROM 's3://condesa/FR.txt'
iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
DELIMITER AS '\t'
;

COPY public.zipcode_nz
FROM 's3://condesa/NZ.txt'
iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
DELIMITER AS '\t'
;

COPY public.zipcode_jp
FROM 's3://condesa/JP.txt'
iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
DELIMITER AS '\t'
;

COPY public.zipcode_ph
FROM 's3://condesa/PH.txt'
iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
DELIMITER AS '\t'
;

COPY public.zipcode_th
FROM 's3://condesa/TH.txt'
iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
DELIMITER AS '\t'
;

-- UNLOAD to S3
-- UNLOAD ('SELECT * FROM public.zipcode_us')
-- TO 's3://bangkok/us_zipcode'
-- iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
-- DELIMITER AS '\t'
-- MANIFEST ALLOWOVERWRITE
-- ;

-- UNLOAD ('SELECT * FROM public.zipcode_ca')
-- TO 's3://bangkok/ca_zipcode'
-- iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
-- DELIMITER AS '\t'
-- MANIFEST ALLOWOVERWRITE
-- ;

-- UNLOAD ('SELECT * FROM public.zipcode_mx')
-- TO 's3://bangkok/mx_zipcode'
-- iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
-- DELIMITER AS '\t'
-- MANIFEST ALLOWOVERWRITE
-- ;

-- UNLOAD ('SELECT * FROM public.zipcode_gb')
-- TO 's3://bangkok/gb_zipcode'
-- iam_role 'arn:aws:iam::517533378855:role/redshift-s3-read-write-role'
-- DELIMITER AS '\t'
-- MANIFEST ALLOWOVERWRITE
-- ;