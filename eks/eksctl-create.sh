#!/bin/bash

set -o nounset

declare START_TIME=$(date +%s)

echo "Creating cluster ${EKS_CLUSTER_NAME} in ${EKS_REGION}"

# NOTE: EMR Studio does not currently support Amazon EMR on EKS when you use
# an AWS Fargate-only Amazon EKS cluster.
# m5.xlarge: 4 vCPU, 16 GB RAM
# m5.2xlarge: 8 vCPU, 32 GB RAM
eksctl create cluster \
    --name="${EKS_CLUSTER_NAME}" \
    --region="${EKS_REGION}" \
    --version="1.19" \
    --nodegroup-name="ng-1" \
    --managed \
    --instance-types="m5.xlarge" \
    --nodes=4 \
    --node-volume-size=80
#    --with-oidc

# OR: Inspired by https://github.com/aws-samples/amazon-eks-apache-spark-etl-sample/blob/master/example/eksctl.yaml
# eksctl create cluster \
#     --config-file=./cluster_config/spark-cluster.yaml

# Enable Cloudwatch
# eksctl utils update-cluster-logging \
#     --name="${EKS_CLUSTER_NAME}" \
#     --region="${EKS_REGION}" \
#     --enable-types=all

echo "Creating AWS client config secrets"
kubectl create secret generic \
    aws-client-secret \
    -n default \
    --from-literal=AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    --from-literal=AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    --from-literal=AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION

echo "Creating AWS s3 config secrets"
kubectl create secret generic \
    aws-s3-secret \
    -n default \
    --from-literal=P3_BUCKET=$P3_BUCKET \
    --from-literal=S3_PREFIX=$S3_PREFIX \
    --from-literal=P3_AWS_ACCESS_KEY=$P3_AWS_ACCESS_KEY \
    --from-literal=P3_AWS_SECRET_KEY=$P3_AWS_SECRET_KEY \
    --from-literal=BK_AWS_ACCESS_KEY=$BK_AWS_ACCESS_KEY \
    --from-literal=BK_AWS_SECRET_KEY=$BK_AWS_SECRET_KEY \
    --from-literal=CO_AWS_ACCESS_KEY=$CO_AWS_ACCESS_KEY \
    --from-literal=CO_AWS_SECRET_KEY=$CO_AWS_SECRET_KEY

echo "Creating AWS db connection secrets"
kubectl create secret generic \
    aws-connect-secret \
    -n default \
    --from-literal=IAM_REDSHIFT=$IAM_REDSHIFT \
    --from-literal=REDSHIFT_DB_URL=$REDSHIFT_DB_URL \
    --from-literal=POSTGRES_DB_URL=$POSTGRES_DB_URL \
    --from-literal=TARGET_JDBC_URL=$TARGET_JDBC_URL

# echo "Creating Azure file shares secret for ${AZ_STORAGE_ACCOUNT_NAME}"
# kubectl create secret generic \
#     az-file-secret \
#     -n ${EKS_NAMESPACE} \
#     --from-literal=azurestorageaccountname=${AZ_STORAGE_ACCOUNT_NAME} \
#     --from-literal=azurestorageaccountkey=${AZ_STORAGE_ACCOUNT_KEY}

declare END_TIME=$(date +%s)
echo "Executed script in $(( (${END_TIME}-${START_TIME})/60 )) minutes"

set +o nounset
