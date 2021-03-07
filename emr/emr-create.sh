#!/bin/bash

declare START_TIME=$(date +%s)
declare VCLUSTER_ID=$(aws emr-containers list-virtual-clusters | jq -r .virtualClusters[0].id)

echo "Creating EMR virtual cluster ${EMR_VCLUSTER_NAME} on ${EKS_CLUSTER_NAME}"
aws emr-containers create-virtual-cluster \
    --name "${EMR_VCLUSTER_NAME}" \
    --container-provider '{
        "id": "'"${EKS_CLUSTER_NAME}"'",
        "type": "EKS",
        "info": {
            "eksInfo": {
                "namespace": "'"${EMR_ON_EKS_NAMESPACE}"'"
            }
        }
    }'

aws emr-containers list-virtual-clusters

declare END_TIME=$(date +%s)
echo "Executed script in $(( (${END_TIME}-${START_TIME})/60 )) minutes"
