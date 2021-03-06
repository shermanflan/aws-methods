#!/bin/bash

set -u

declare START_TIME=$(date +%s)

echo "Creating cluster ${EKS_CLUSTER_NAME} in ${EKS_REGION}"

eksctl create cluster \
--name "${EKS_CLUSTER_NAME}" \
--region "${EKS_REGION}" \
--fargate

declare END_TIME=$(date +%s)
echo "Executed script in $(( (${END_TIME}-${START_TIME})/60 )) minutes"
