#!/bin/bash

set -u

declare START_TIME=$(date +%s)

aws emr-containers create-virtual-cluster \
    --name "${EMR_VCLUSTER_NAME}" \
    --container-provider '{
        "id": "cluster_name",
        "type": "EKS",
        "info": {
            "eksInfo": {
                "namespace": "${EMR_ON_EKS_NAMESPACE}"
            }
        }
    }'

declare END_TIME=$(date +%s)
echo "Executed script in $(( (${END_TIME}-${START_TIME})/60 )) minutes"
