#!/bin/bash 

set -o nounset

declare REGISTRY_ID=$(aws ecr describe-registry | jq -r .registryId)

aws ecr delete-repository \
    --registry-id ${REGISTRY_ID} \
    --repository-name ${AZ_PYSPARK_IMAGE} \
    --force

aws ecr delete-repository \
    --registry-id ${REGISTRY_ID} \
    --repository-name ${AZ_PYSPARK_APP_IMAGE} \
    --force

echo "Removing tagged image [${AZ_PYSPARK_IMAGE}]"
docker image rm \
    ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${AZ_PYSPARK_IMAGE}:${AZ_PYSPARK_IMAGE_VERSION}

echo "Removing tagged image [${AZ_PYSPARK_APP_IMAGE}]"
docker image rm \
    ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${AZ_PYSPARK_APP_IMAGE}:${AZ_PYSPARK_APP_IMAGE_VERSION}

set +o nounset
