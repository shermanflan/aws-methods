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

echo "Removing tagged image [${PYSPARK_IMAGE}]"
docker image rm \
    ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${PYSPARK_IMAGE}:${PYSPARK_IMAGE_VERSION}

echo "Removing tagged image [${PYSPARK_APP_IMAGE}]"
docker image rm \
    ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${PYSPARK_APP_IMAGE}:${PYSPARK_APP_IMAGE_VERSION}


set +o nounset
