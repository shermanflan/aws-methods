#!/bin/bash

set -u

echo "Creating EMR cluster IAM mapping on ${EKS_CLUSTER_NAME}"
eksctl create iamidentitymapping \
    --cluster "${EKS_CLUSTER_NAME}" \
    --namespace "${EMR_ON_EKS_NAMESPACE}" \
    --service-name "emr-containers"


echo "Create EMR job execution role"
aws iam create-role \
   --role-name emr-job-execution-role \
   --assume-role-policy-document '{
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
            "Service": "emr-containers.amazonaws.com"
          },
         "Action": "sts:AssumeRole"
       }
     ] 
   }'

echo "Create IAM Roles for Service Accounts on ${EKS_CLUSTER_NAME}"
eksctl utils associate-iam-oidc-provider \
    --cluster "${EKS_CLUSTER_NAME}" \
    --approve

echo "Create EMR job execution policy"
aws iam create-policy \
   --policy-name emr-job-execution-policy \
   --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket"
            ],
         "Resource": [
           "arn:aws:s3:::condesa", 
           "arn:aws:s3:::condesa/*",
           "arn:aws:s3:::bangkok", 
           "arn:aws:s3:::bangkok/*"
         ] 
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:PutLogEvents",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams"
            ],
            "Resource": [
                "arn:aws:logs:*:*:*"
            ]
        }
    ]
}'

echo "Attach EMR role to EMR policy"
aws iam attach-role-policy \
   --policy-arn arn:aws:iam::517533378855:policy/emr-job-execution-policy \
   --role-name emr-job-execution-role

echo "Update trust policy of the EMR job execution role"
# aws rds add-role-to-db-instance \
#    --db-instance-identifier ${PG_INSTANCE} \
#    --feature-name s3Import \
#    --role-arn arn:aws:iam::517533378855:role/rds-s3-import-role \
#    --region us-east-2
aws emr-containers update-role-trust-policy \
    --cluster-name "${EKS_CLUSTER_NAME}" \
    --namespace "${EMR_ON_EKS_NAMESPACE}" \
    --role-name emr-job-execution-role
