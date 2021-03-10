#!/bin/bash

declare VCLUSTER_ID=$(aws emr-containers list-virtual-clusters | jq .virtualClusters | jq '.[] | select(.state == "RUNNING")' | jq -r .id)

# TODO: Delete private CA and certs
# Checkpoint
aws emr-containers create-managed-endpoint \
    --type JUPYTER_ENTERPRISE_GATEWAY \
    --virtual-cluster-id ${VCLUSTER_ID} \
    --name ${EMR_ENDPOINT_NAME} \
    --execution-role-arn "arn:aws:iam::517533378855:policy/emr-job-execution-policy" \
    --release-label emr-6.2.0-latest
    --certificate-arn "arn:aws:acm:us-east-2:517533378855:certificate/f4dbd279-06da-43fd-ac63-aa76c188f663"