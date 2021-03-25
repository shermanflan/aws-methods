#!/bin/bash

set -o nounset

echo "Creating repository [${PYSPARK_IMAGE}]"
aws ecr create-repository \
    --repository-name ${PYSPARK_IMAGE} \
    --image-scanning-configuration scanOnPush=false

echo "Creating repository [${PYSPARK_APP_IMAGE}]"
aws ecr create-repository \
    --repository-name ${PYSPARK_APP_IMAGE} \
    --image-scanning-configuration scanOnPush=false

declare REGISTRY_ID=$(aws ecr describe-registry | jq -r .registryId)

echo "Authentiating Docker to [${REGISTRY_ID}]"
aws ecr get-login-password --region ${REGION} | \
    docker login \
        --username AWS \
        --password-stdin ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com

echo "Tagging image [${PYSPARK_IMAGE}]"
docker tag ${PYSPARK_IMAGE}:${PYSPARK_IMAGE_VERSION} \
    ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${PYSPARK_IMAGE}:${PYSPARK_IMAGE_VERSION}

echo "Pusing image [${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${PYSPARK_IMAGE}:${PYSPARK_IMAGE_VERSION}]"
docker push ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${PYSPARK_IMAGE}:${PYSPARK_IMAGE_VERSION}

echo "Tagging image [${PYSPARK_APP_IMAGE}]"
docker tag ${PYSPARK_APP_IMAGE}:${PYSPARK_APP_IMAGE_VERSION} \
    ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${PYSPARK_APP_IMAGE}:${PYSPARK_APP_IMAGE_VERSION}

echo "Pusing image [${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${PYSPARK_APP_IMAGE}:${PYSPARK_APP_IMAGE_VERSION}]"
docker push ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${PYSPARK_APP_IMAGE}:${PYSPARK_APP_IMAGE_VERSION}

echo "Describe images"
aws ecr describe-repositories

aws ecr describe-images --repository-name ${PYSPARK_IMAGE}
aws ecr list-images \
    --registry-id ${REGISTRY_ID} \
    --repository-name ${PYSPARK_IMAGE}

aws ecr describe-images --repository-name ${PYSPARK_APP_IMAGE}
aws ecr list-images \
    --registry-id ${REGISTRY_ID} \
    --repository-name ${PYSPARK_APP_IMAGE}

# echo "Pulling image [${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:${VERSION}]"
# docker pull ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:${VERSION}

set +o nounset
