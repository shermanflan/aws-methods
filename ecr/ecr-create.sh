#!/bin/bash

set -o nounset

echo "Creating repository [${REPO_NAME}]"
aws ecr create-repository \
    --repository-name ${REPO_NAME} \
    --image-scanning-configuration scanOnPush=false
    # --generate-cli-skeleton

declare REGISTRY_ID=$(aws ecr describe-registry | jq -r .registryId)

echo "Authentiating Docker to [${REGISTRY_ID}]"
aws ecr get-login-password --region ${REGION} | \
    docker login \
        --username AWS \
        --password-stdin ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com

echo "Tagging image [${IMAGE}]"
docker tag ${IMAGE}:${VERSION} ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:${VERSION}

echo "Pusing image [${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:${VERSION}]"
docker push ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:${VERSION}

echo "Describe images"
aws ecr describe-repositories
aws ecr describe-images --repository-name ${REPO_NAME}
aws ecr list-images \
    --registry-id ${REGISTRY_ID} \
    --repository-name ${REPO_NAME}

echo "Pulling image [${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:${VERSION}]"
docker pull ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${REPO_NAME}:${VERSION}

set +o nounset
