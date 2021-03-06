#!/bin/bash 

set -u

declare REGISTRY_ID=$(aws ecr describe-registry | jq -r .registryId)

aws ecr delete-repository \
    --registry-id ${REGISTRY_ID} \
    --repository-name ${REPO_NAME} \
    --force