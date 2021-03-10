#!/bin/bash

aws emr-containers delete-managed-endpoint \
    --endpoint-id <managed-endpoint-id> \
    --virtual-cluster-id <virtual-cluster-id>
