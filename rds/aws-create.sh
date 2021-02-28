#!/bin/bash -eux

aws rds create-db-instance \
    --db-name ${DB_NAME} \
    --db-instance-identifier ${PG_INSTANCE} \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username ${PG_USER} \
    --master-user-password ${PG_PASSWORD} \
    --allocated-storage 20 \
    --publicly-accessible

psql --username=${PG_USER} \
    --password \
    --host=${PG_INSTANCE} \
    --dbname=${DB_NAME} \
    --port=5432 \
    --command="CREATE EXTENSION aws_s3 CASCADE;"

# Clean up
# aws iam delete-role --role-name rds-s3-import-role
# aws iam detach-role-policy \
# --role-name rds-s3-import-role \
# --policy-arn "arn:aws:iam::517533378855:policy/rds-s3-import-policy"
# aws iam delete-role-policy \
#     --role-name rds-s3-import-role \
#     --policy-name rds-s3-import-policy
# aws iam delete-policy --policy-arn "arn:aws:iam::517533378855:policy/rds-s3-import-policy"

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
#    --policy-arn arn:aws:iam::517533378855:policy/rds-s3-import-policy \
#    --role-name rds-s3-import-role

# TODO: Wait for rds instance
echo "Add role to RDS instance"
aws rds add-role-to-db-instance \
   --db-instance-identifier rkoinstance-3 \
   --feature-name s3Import \
   --role-arn arn:aws:iam::517533378855:role/rds-s3-import-role \
   --region us-east-2
