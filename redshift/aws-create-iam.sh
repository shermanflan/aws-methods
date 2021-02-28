#!/bin/bash -eux

echo "Create Redshift access to S3 policies"
"arn:aws:iam::517533378855:policy/redshift-s3-read-policy"
aws iam create-policy \
   --policy-name redshift-s3-read-policy \
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

"arn:aws:iam::517533378855:policy/redshift-s3-write-policy"
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

echo "Create Redshift role"
"arn:aws:iam::517533378855:role/redshift-s3-read-write-role"
aws iam create-role \
   --role-name redshift-s3-read-write-role \
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

echo "Attach Redshift roles to S3 policy"
aws iam attach-role-policy \
   --policy-arn arn:aws:iam::517533378855:policy/redshift-s3-read-policy \
   --role-name redshift-s3-read-write-role

aws iam attach-role-policy \
   --policy-arn arn:aws:iam::517533378855:policy/redshift-s3-write-policy \
   --role-name redshift-s3-read-write-role

echo "Add role to Redshift instance"
aws redshift modify-cluster-iam-roles \
    --cluster-identifier "${REDSHIFT_INSTANCE}" \
    --add-iam-roles "arn:aws:iam::517533378855:role/redshift-s3-read-write-role"
