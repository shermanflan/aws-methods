# Spark on Kubernetes
This repo contains a reference implementation for deploying Spark 3.1.1
on Kubernetes.

## References
- [spark-submit](http://spark.apache.org/docs/latest/submitting-applications.html)
- [Spark on Kubernetes](http://spark.apache.org/docs/latest/running-on-kubernetes.html)

# Building Spark 3.1.1 Images
In order to run Spark on k8s, docker images for the respective distribution
need to be build and deployed to ECR. Reference Docker images and tools
can be found from the Spark [distribution](https://spark.apache.org/downloads.html).

1. Build base container
```shell
./bin/docker-image-tool.sh -t 3.1.1 build
```
2. Build base container with Python bindings (PySpark)
```shell
./bin/docker-image-tool.sh -t 3.1.1 \
  -p ./kubernetes/dockerfiles/spark/bindings/python/Dockerfile build
```
3. Bundle a Python application image with specific dependencies based on 
   the base container. This will be used to run the spark-submit job in k8s.
   See the [Dockerfile](./Dockerfile) for reference.

# Technical Pre-requisites

- The service account credentials used by the driver pods must be allowed 
  to create pods, services and configmaps.
- 

# Smoke Tests
- Run SparkPi
```shell
./bin/run-example SparkPi 10
```
- Run pi.py
```shell
./bin/spark-submit examples/src/main/python/pi.py 10
```