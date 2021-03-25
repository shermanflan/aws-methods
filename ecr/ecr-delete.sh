#!/bin/bash 

set -o nounset

declare REGISTRY_ID=$(aws ecr describe-registry | jq -r .registryId)

aws ecr delete-repository \
    --registry-id ${REGISTRY_ID} \
    --repository-name ${PYSPARK_IMAGE} \
    --force

aws ecr delete-repository \
    --registry-id ${REGISTRY_ID} \
    --repository-name ${PYSPARK_APP_IMAGE} \
    --force

set +o nounset
