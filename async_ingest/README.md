# Bulk Data Extraction/Import
This repo demonstrates a possible approach for bulk extraction of data 
from Redshift intto a postgres database using native AWS-features. In 
order to reduce time spent on blocking I/O, the `asyncio` library is used
when invoking these features from Python.

## Bulk Export from Redshift
Redshift supports the [`UNLOAD`](https://docs.aws.amazon.com/redshift/latest/dg/r_UNLOAD.html) 
operator which allows export of any SQL statement to S3. Multiple file 
formats are supported, including Parquet, as well as various compression 
schemes. 

In this proof of concept, TSV-formatted exports are used in order to remain
compatible with postgresql. For example, the command below exports the data
contained in `public.zipcode_us` to the specified s3 location in tab-delimited 
format.

```
UNLOAD ('SELECT * FROM public.zipcode_us')
TO 's3://bangkok/us_zipcode/us_'
iam_role 'arn:aws:iam::123456789:role/my-s3-write-role'
DELIMITER AS '\t'
MANIFEST ALLOWOVERWRITE
```

### Security Considerations
In order to use the `UNLOAD` operator, an IAM policy needs to be defined 
with write access to the specified S3 bucket. This policy then needs to be
associated to an IAM role for Redshift. A sample policy and role is shown
below. For the full AWS CLI commands, refer to the 
[`aws-create-iam.sh`](../redshift/aws-create-iam.sh) script.

```shell
aws iam create-policy \
   --policy-name redshift-s3-write-policy \
   --policy-document '{
      "Version": "2012-10-17",
      "Statement": [
       {
          "Sid": "s3export",
          "Action": [
            "s3:PutObject"
          ],
          "Effect": "Allow",
          "Resource": [
            "arn:aws:s3:::condesa", 
            "arn:aws:s3:::condesa/*",
            "arn:aws:s3:::bangkok", 
            "arn:aws:s3:::bangkok/*"
          ] 
        }
      ] 
    }'
```

```shell
aws iam create-role \
  --role-name my-s3-write-role \
  --assume-role-policy-document '{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "redshift.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ] 
    }'
```

## Postgresql (RDS) Bulk Import
Similarly, postgresql on AWS RDS supports the 
[`aws_s3.table_import_from_s3`](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Procedural.Importing.html#USER_PostgreSQL.S3Import),
function which can be used to bulk import from an S3 location. At this 
time, only text-delimited formats are supported (compressed or 
non-compressed).

For example, the command below imports the file located at S3 bucket 
`condesa` to the table `public.zipcode`.

```
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
```

### Configuration
In order to use the `aws_s3.table_import_from_s3` function, the following
extension needs to be installed on the RDS instance.

```shell
psql --username=${PG_USER} \
    --password \
    --host=${PG_INSTANCE_FQDN} \
    --dbname=${DB_NAME} \
    --port=5432 \
    --command="CREATE EXTENSION aws_s3 CASCADE;"
```

### Security Considerations
Similarly, an IAM policy and role needs to be created for the postgresql
instance granting it permission to read from the respective S3 bucket(s).

A sample role and policy is shown below. Refer to the [rds-create.sh](../rds/rds-create.sh) 
script for the complete AWS CLI commands.

```shell
aws iam create-policy \
   --policy-name rds-s3-import-policy \
   --policy-document '{
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "s3import",
         "Action": [
           "s3:GetObject",
           "s3:ListBucket"
         ],
         "Effect": "Allow",
         "Resource": [
           "arn:aws:s3:::condesa", 
           "arn:aws:s3:::condesa/*",
           "arn:aws:s3:::bangkok", 
           "arn:aws:s3:::bangkok/*"
         ] 
       }
     ] 
   }'
```

```shell
aws iam create-role \
   --role-name rds-s3-import-role \
   --assume-role-policy-document '{
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
            "Service": "rds.amazonaws.com"
          },
         "Action": "sts:AssumeRole"
       }
     ] 
   }'
```

## Asynchronous IO
Finally, in order to support higher throughput given the nature of these
synchronous export/import invocations, the [`asyncio`](https://docs.python.org/3/library/asyncio.html)
library is used to spawn additional non-blocking threads as needed. Initial 
tests have shown a significant reduction in overall load time using this 
approach.

An example is shown below demonstrating both extract and load calls being
spawned into separate non-blocking sub-processes. For full details, refer
to the [etl.py](ingest/etl.py) script.

```python
async def acquire_async(source, target, lake) -> None:
    tasks = starmap(_acquire_async, [(source, target, lake, *config.values())
                                     for config in ETL_MAPPING[:]])

    await asyncio.gather(*tasks)


async def _acquire_async(source, target, lake, table: str, sql: str,
                         lake_path: str) -> None:

    await asyncio.gather(
        asyncio.to_thread(unloader, source, sql, lake_path)
    )

    parts = urlparse(lake_path)
    exports = lake.list_objects_v2(Bucket=parts.hostname,
                                   Prefix=parts.path[1:])

    load_tasks = (
        asyncio.to_thread(loader, target, table, parts.hostname, part['Key'])
        for part in exports.get('Contents', [])
        if not part['Key'].endswith('manifest') and part['Size'] > 0
    )

    await asyncio.gather(*load_tasks)
```