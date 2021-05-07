#!/bin/bash

set -o nounset

# Pricing: https://aws.amazon.com/rds/postgresql/pricing/?pg=pr&loc=3
# db.t3.micro: 0.018 $/hr
# db.t3.large: 0.145 $/hr
aws rds create-db-instance \
    --db-name ${DB_NAME} \
    --db-instance-identifier ${PG_INSTANCE} \
    --db-instance-class db.t3.large \
    --engine postgres \
    --master-username ${PG_USER} \
    --master-user-password ${PG_PASSWORD} \
    --allocated-storage 80 \
    --publicly-accessible
    # --engine-version 11.4

# Clean up
# aws iam delete-role --role-name rds-s3-import-role
# aws iam detach-role-policy \
# --role-name rds-s3-import-role \
# --policy-arn "arn:aws:iam::[123456789]:policy/rds-s3-import-policy"
# aws iam delete-role-policy \
#     --role-name rds-s3-import-role \
#     --policy-name rds-s3-import-policy
# aws iam delete-policy --policy-arn "arn:aws:iam::123456789:policy/rds-s3-import-policy"

# echo "Create RDS access to S3 policy"
# aws iam create-policy \
#    --policy-name rds-s3-import-policy \
#    --policy-document '{
#      "Version": "2012-10-17",
#      "Statement": [
#        {
#          "Sid": "s3import",
#          "Action": [
#            "s3:GetObject",
#            "s3:ListBucket"
#          ],
#          "Effect": "Allow",
#          "Resource": [
#            "arn:aws:s3:::condesa", 
#            "arn:aws:s3:::condesa/*",
#            "arn:aws:s3:::bangkok", 
#            "arn:aws:s3:::bangkok/*"
#          ] 
#        }
#      ] 
#    }'

# echo "Create RDS role"
# aws iam create-role \
#    --role-name rds-s3-import-role \
#    --assume-role-policy-document '{
#      "Version": "2012-10-17",
#      "Statement": [
#        {
#          "Effect": "Allow",
#          "Principal": {
#             "Service": "rds.amazonaws.com"
#           },
#          "Action": "sts:AssumeRole"
#        }
#      ] 
#    }'

# echo "Attach RDS role to S3 policy"
# aws iam attach-role-policy \
#    --policy-arn arn:aws:iam::123456789:policy/rds-s3-import-policy \
#    --role-name rds-s3-import-role

declare -i max_tries=100
declare DB_READY=$(aws rds describe-db-instances --db-instance-identifier ${PG_INSTANCE} | jq -r .DBInstances[0].DBInstanceStatus)

while [[ ${DB_READY} != "available" && ${max_tries} -gt 0 ]]
    do

    echo "${DB_READY}: Waiting for ${PG_INSTANCE} (${max_tries})"
    sleep 10

    DB_READY=$(aws rds describe-db-instances --db-instance-identifier ${PG_INSTANCE} | jq -r .DBInstances[0].DBInstanceStatus)
    ((max_tries = max_tries - 1))
done

# echo 'Create aws_s3 extention'
# psql --username=${PG_USER} \
#     --password \
#     --host=${PG_INSTANCE_FQDN} \
#     --dbname=${DB_NAME} \
#     --port=5432 \
#     --command="CREATE EXTENSION aws_s3 CASCADE;"

# echo 'Create database tables'
# psql --username=${PG_USER} \
#     --password \
#     --host=${PG_INSTANCE_FQDN} \
#     --dbname=${DB_NAME} \
#     --port=5432 \
#     --file ./create-db.sql

# echo "Add role to RDS instance"
# aws rds add-role-to-db-instance \
#    --db-instance-identifier ${PG_INSTANCE} \
#    --feature-name s3Import \
#    --role-arn arn:aws:iam::123456789:role/rds-s3-import-role \
#    --region us-east-2

set +o nounset
