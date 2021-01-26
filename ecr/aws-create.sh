#!/bin/bash -eux

# echo "Creating repository [${REPO_NAME}]"
# aws ecr create-repository \
#     --repository-name ${REPO_NAME} \
#     --image-scanning-configuration scanOnPush=true
    # --generate-cli-skeleton

declare REGISTRY_ID=$(aws ecr describe-registry | jq -r .registryId)

echo "Authentiating Docker to [${REGISTRY_ID}]"
aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com

echo "Tagging image [${IMAGE}]"
docker tag ${IMAGE}:${VERSION} ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${IMAGE}:${VERSION}

echo "Pusing image [${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${IMAGE}:${VERSION}]"
docker push ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${IMAGE}:${VERSION}

echo "Describe images"
aws ecr describe-repositories
aws ecr describe-images --repository-name ${IMAGE}

# aws ecr list-images \
#     --registry-id ${REGISTRY_ID} \
#     --repository-name ${IMAGE}

echo "Pulling image [${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${IMAGE}:${VERSION}]"
docker pull ${REGISTRY_ID}.dkr.ecr.${REGION}.amazonaws.com/${IMAGE}:${VERSION}