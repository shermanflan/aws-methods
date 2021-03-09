#!/bin/bash

declare START_TIME=$(date +%s)

echo "Creating cluster ${EKS_CLUSTER_NAME} in ${EKS_REGION}"

eksctl create cluster \
    --name "${EKS_CLUSTER_NAME}" \
    --region "${EKS_REGION}" \
    --version 1.19 \
    --fargate

declare END_TIME=$(date +%s)
echo "Executed script in $(( (${END_TIME}-${START_TIME})/60 )) minutes"
