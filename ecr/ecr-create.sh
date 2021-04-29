#!/bin/bash

set -o nounset

echo "Creating repository [${AWS_PYSPARK_IMAGE}]"
aws ecr create-repository \
    --repository-name ${AWS_PYSPARK_IMAGE} \
    --image-scanning-configuration scanOnPush=false

echo "Creating repository [${AWS_PYSPARK_APP_IMAGE}]"
aws ecr create-repository \
    --repository-name ${AWS_PYSPARK_APP_IMAGE} \
    --image-scanning-configuration scanOnPush=false

declare REGISTRY_ID=$(aws ecr describe-registry | jq -r .registryId)

echo "Authentiating Docker to [${REGISTRY_ID}]"
aws ecr get-login-password --region ${REGION} | \
    docker login \
        --username AWS \
        --password-stdin ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com

echo "Tagging image [${AWS_PYSPARK_IMAGE}]"
docker tag ${AWS_PYSPARK_IMAGE}:${AWS_PYSPARK_IMAGE_VERSION} \
    ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${AWS_PYSPARK_IMAGE}:${AWS_PYSPARK_IMAGE_VERSION}

echo "Pushing image [${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${AWS_PYSPARK_IMAGE}:${AWS_PYSPARK_IMAGE_VERSION}]"
docker push ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${AWS_PYSPARK_IMAGE}:${AWS_PYSPARK_IMAGE_VERSION}

# echo "Removing tagged image [${AWS_PYSPARK_APP_IMAGE}]"
# docker image rm \
#     ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${AWS_PYSPARK_APP_IMAGE}:${AWS_PYSPARK_APP_IMAGE_VERSION}

echo "Tagging image [${AWS_PYSPARK_APP_IMAGE}]"
docker tag ${AWS_PYSPARK_APP_IMAGE}:${AWS_PYSPARK_APP_IMAGE_VERSION} \
    ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${AWS_PYSPARK_APP_IMAGE}:${AWS_PYSPARK_APP_IMAGE_VERSION}

echo "Pushing image [${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${AWS_PYSPARK_APP_IMAGE}:${AWS_PYSPARK_APP_IMAGE_VERSION}]"
docker push ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${AWS_PYSPARK_APP_IMAGE}:${AWS_PYSPARK_APP_IMAGE_VERSION}

# echo "Describe images"
# aws ecr describe-repositories

# aws ecr describe-images --repository-name ${PYSPARK_APP_IMAGE}
# aws ecr list-images \
#     --registry-id ${REGISTRY_ID} \
#     --repository-name ${PYSPARK_APP_IMAGE}

# echo "Pulling image [${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:${VERSION}]"
# docker pull ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:${VERSION}

set +o nounset
