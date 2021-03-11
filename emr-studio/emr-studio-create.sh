#!/bin/bash

declare VCLUSTER_ID=$(aws emr-containers list-virtual-clusters | jq .virtualClusters | jq '.[] | select(.state == "RUNNING")' | jq -r .id)

# TODO: Delete private CA and certs
# Checkpoint
aws emr-containers create-managed-endpoint \
    --type JUPYTER_ENTERPRISE_GATEWAY \
    --virtual-cluster-id ${VCLUSTER_ID} \
    --name ${EMR_ENDPOINT_NAME} \
    --execution-role-arn ${EMR_EXECUTION_ROLE_ARN} \
    --release-label emr-6.2.0-latest \
    --certificate-arn ${EMR_STUDIO_CA_ARN}

aws emr-containers list-managed-endpoints \
    --virtual-cluster-id ${VCLUSTER_ID}

declare ENDPOINT_ID=$(aws emr-containers list-managed-endpoints --virtual-cluster-id ${VCLUSTER_ID} | jq -r .endpoints[0].id)

aws emr-containers describe-managed-endpoint \
    --id ${ENDPOINT_ID} \
    --virtual-cluster-id ${VCLUSTER_ID}
