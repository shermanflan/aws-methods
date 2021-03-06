#!/bin/bash

set -o nounset

# Clean up
echo "Deleting cluster ${EKS_CLUSTER_NAME}"
eksctl delete cluster \
    --name "${EKS_CLUSTER_NAME}" \
    --region "${EKS_REGION}"

set +o nounset
