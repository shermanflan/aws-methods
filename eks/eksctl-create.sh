#!/bin/bash

set -o nounset

declare START_TIME=$(date +%s)

echo "Creating cluster ${EKS_CLUSTER_NAME} in ${EKS_REGION}"

# NOTE: EMR Studio does not currently support Amazon EMR on EKS when you use
# an AWS Fargate-only Amazon EKS cluster.
eksctl create cluster \
    --name="${EKS_CLUSTER_NAME}" \
    --region="${EKS_REGION}" \
    --version="1.19" \
    --nodegroup-name="ng-1" \
    --managed \
    --instance-types="m5.xlarge" \
    --nodes=2 \
    --node-volume-size=40
#    --with-oidc

# OR:
# eksctl create cluster \
#     --config-file=./cluster_config/basic-cluster.yaml

# Enable Cloudwatch
# eksctl utils update-cluster-logging \
#     --name="${EKS_CLUSTER_NAME}" \
#     --region="${EKS_REGION}" \
#     --enable-types=all

declare END_TIME=$(date +%s)
echo "Executed script in $(( (${END_TIME}-${START_TIME})/60 )) minutes"

set +o nounset
