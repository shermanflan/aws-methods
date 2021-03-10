#!/bin/bash

echo "Creating namespace ${EMR_ON_EKS_NAMESPACE} on ${EKS_CLUSTER_NAME}"
kubectl create namespace "${EMR_ON_EKS_NAMESPACE}"
kubectl get ns

echo "Creating EMR cluster IAM mapping on ${EKS_CLUSTER_NAME}"
eksctl create iamidentitymapping \
  --cluster "${EKS_CLUSTER_NAME}" \
  --namespace "${EMR_ON_EKS_NAMESPACE}" \
  --service-name "emr-containers"

echo "Get OID Connect issuer URL for ${EKS_CLUSTER_NAME}"
aws eks describe-cluster \
  --name "${EKS_CLUSTER_NAME}" \
  --query "cluster.identity.oidc.issuer" \
  --output text

echo "Create OIDC identity provider mapping for ${EKS_CLUSTER_NAME}"
eksctl utils associate-iam-oidc-provider \
  --cluster "${EKS_CLUSTER_NAME}" \
  --approve

# One-time
# echo "Create EMR job execution role"
# aws iam create-role \
#    --role-name emr-job-execution-role \
#    --assume-role-policy-document '{
#     "Version": "2012-10-17",
#     "Statement": [
#       {
#         "Effect": "Allow",
#         "Principal": {
#           "Service": "emr-containers.amazonaws.com"
#         },
#         "Action": "sts:AssumeRole"
#       }
#     ] 
#   }'

# One-time: use create-policy
# To Update: issue create-policy-version (max 5)
# echo "Delete EMR job execution policy version"
# aws iam delete-policy-version \
#   --policy-arn arn:aws:iam::517533378855:policy/emr-job-execution-policy \
#   --version-id v4

# echo "Create/Update EMR job execution policy"
# aws iam create-policy-version \
#   --set-as-default \
#   --policy-arn arn:aws:iam::517533378855:policy/emr-job-execution-policy \
#   --policy-document '{
#   "Version": "2012-10-17",
#   "Statement": [
#       {
#         "Effect": "Allow",
#         "Action": [
#           "s3:PutObject",
#           "s3:GetObject",
#           "s3:ListBucket",
#           "s3:CreateBucket"
#         ],
#         "Resource": [
#           "arn:aws:s3:::condesa",
#           "arn:aws:s3:::condesa/*",
#           "arn:aws:s3:::bangkok",
#           "arn:aws:s3:::bangkok/*",
#           "arn:aws:s3:::r5o-spark-logs",
#           "arn:aws:s3:::r5o-spark-logs/*", 
#           "arn:aws:s3:::r5o-spark-jobs",
#           "arn:aws:s3:::r5o-spark-jobs/*"
#         ]
#       },
#       {
#         "Effect": "Allow",
#         "Action": [
#             "logs:PutLogEvents",
#             "logs:CreateLogStream",
#             "logs:DescribeLogGroups",
#             "logs:DescribeLogStreams",
#             "logs:CreateLogGroup"
#         ],
#         "Resource": [
#             "arn:aws:logs:*:*:*"
#         ]
#       }
#     ]
#   }'

# One-time
# echo "Attach EMR role to EMR policy"
# aws iam attach-role-policy \
#    --policy-arn arn:aws:iam::517533378855:policy/emr-job-execution-policy \
#    --role-name emr-job-execution-role

echo "Update trust policy of the EMR job execution role"
aws emr-containers update-role-trust-policy \
  --cluster-name "${EKS_CLUSTER_NAME}" \
  --namespace "${EMR_ON_EKS_NAMESPACE}" \
  --role-name emr-job-execution-role

# echo "Create fargate profile for pods in ${EMR_ON_EKS_NAMESPACE}"
# eksctl create fargateprofile \
#   --cluster "${EKS_CLUSTER_NAME}" \
#   --name "${EMR_FARGATE_PROFILE}" \
#   --namespace "${EMR_ON_EKS_NAMESPACE}"  
