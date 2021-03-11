#!/bin/bash

declare ENDPOINT_ID=$(aws emr-containers list-managed-endpoints --virtual-cluster-id ${VCLUSTER_ID} | jq -r .endpoints[0].id)

aws emr-containers delete-managed-endpoint \
    --id ${ENDPOINT_ID} \
    --virtual-cluster-id ${VCLUSTER_ID}
