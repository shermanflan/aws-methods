#!/bin/bash

set -o nounset

echo "Creating Azure file shares secret for ${AZ_STORAGE_ACCOUNT_NAME}"
kubectl create secret generic \
    az-file-secret \
    -n ${EKS_NAMESPACE} \
    --from-literal=azurestorageaccountname=${AZ_STORAGE_ACCOUNT_NAME} \
    --from-literal=azurestorageaccountkey=${AZ_STORAGE_ACCOUNT_KEY}

# NOTE: ECR access granted by default when using eksctl
set +o nounset
