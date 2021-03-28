#!/bin/bash

cd ../../spark-3.1.1/spark-3.1.1-bin-hadoop2.7

echo 'Rebuilding standard Spark base image'
./bin/docker-image-tool.sh -t 3.1.1 \
    -n build

echo 'Rebuilding standard spark base image with Python bindings'
./bin/docker-image-tool.sh -t 3.1.1 \
  -p ./kubernetes/dockerfiles/spark/bindings/python/Dockerfile \
    -n build

echo 'Rebuilding Spark application image'
cd ../../apps/spark_ingest
docker build -t spark-ingest:latest --no-cache .