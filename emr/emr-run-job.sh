#!/bin/bash

declare START_TIME=$(date +%s)
declare VCLUSTER_ID=$(aws emr-containers list-virtual-clusters | jq .virtualClusters | jq '.[] | select(.state == "RUNNING")' | jq -r .id)
declare EXECUTION_ROLE_ARN=$(aws iam get-role --role-name ${EMR_EXECUTION_ROLE_NAME} | jq -r .Role.Arn)

# Reference https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/emr-eks-jobs-CLI.html
aws emr-containers start-job-run \
    --virtual-cluster-id "${VCLUSTER_ID}" \
    --execution-role-arn "${EXECUTION_ROLE_ARN}" \
    --cli-input-json file://./jobs/pi-hello-world.json

declare END_TIME=$(date +%s)
echo "Executed script in $(( (${END_TIME}-${START_TIME})/60 )) minutes"
