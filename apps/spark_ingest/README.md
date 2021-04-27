# Spark on Kubernetes
This repo contains a reference implementation for deploying Spark 3.1.1
on Kubernetes.

## References
- [spark-submit](http://spark.apache.org/docs/latest/submitting-applications.html)
- [Spark on Kubernetes](http://spark.apache.org/docs/latest/running-on-kubernetes.html)

# Building Spark 3.1.1 Images
In order to run Spark on k8s, docker images for the respective distribution
need to be built and deployed to ECR. Reference Docker images and tools
can be found from the Spark [distribution](https://spark.apache.org/downloads.html).

1. Build base container
```shell
./bin/docker-image-tool.sh -t 3.1.1 build
```
2. Build base container with Python bindings (PySpark)
    - This base image will be used as the driver container for running the 
      `spark-submit` command in k8s.

```shell
./bin/docker-image-tool.sh -t 3.1.1 \
  -p ./kubernetes/dockerfiles/spark/bindings/python/Dockerfile build
```
3. Bundle a Python application image based on the base container with 
   additional dependencies as needed. This will be used as the executor 
   image for the job in k8s. See the [Dockerfile](./Dockerfile) for reference.

# Technical Pre-requisites

- The service account credentials used by the driver pods must be allowed 
  to create pods, services and configmaps.

# General Spark Configuration

## Logging
To override the default log configuration:

1. Build the container with a `conf` directory in the `$SPARK_HOME`
   directory.
2. Copy the log4j.properties.template provided with the Spark distribution
   into this directory and override as needed.

See [local_config](./local_config/log4j.properties) for a reference example.

## JDBC
The appropriate JDBC driver must be made available to the spark classpath in
order to initiate database i/o.

### Postresql
1. Download the latest [JDBC driver](https://jdbc.postgresql.org/download.html)
   - As of this writing, current version is 42.2.20
2. Copy the respective JAR to the Spark /jars folder
3. Build the Spark 3.1.1 container with Python bindings

# Azure Idiosyncrasies

## Blob Storage
Reading from Blob storage uses the [wasb filesystem protocol](https://github.com/hning86/articles/blob/master/hadoopAndWasb.md).
After navigating the netherworld of Hadoop "*JAR hell*", I have determined
that the following steps are required to successfully configure Spark to 
read from Azure Blob storage.

1. Download [Spark 3.1.1 bundled with Hadoop 2.7](https://spark.apache.org/downloads.html)
2. Download [Hadoop 2.7.4](https://archive.apache.org/dist/hadoop/common/)
3. Extract both to the local filesystem.
4. Copy the following "fat" JARs from Hadoop to the Spark /jars folder
    - hadoop-2.7.4/share/hadoop/tools/lib/hadoop-azure-2.7.4.jar
    - hadoop-2.7.4/share/hadoop/tools/lib/azure-storage-2.0.0.jar
5. Build the Spark 3.1.1 container with Python bindings.

# AWS Idiosyncrasies

## spark-submit
This [reference](https://stackoverflow.com/a/66657993) was invaluable in
getting Spark 3.1.1 on an EKS cluster working.

- In order to successfully submit a spark job on AWS EMR on EKS, the 
  spark-submit parameters should use the `args` stanza instead of `command`
  as the former will route the command through the `entrypoint.sh`. 
- In addition, a config of `spark.jars.ivy=/tmp/.ivy` needs to be supplied
  in the spark-submit parameters.
- See [spark-ingest.yaml](../../eks/pods/spark-ingest.yaml) for a reference. 

## S3
Reading from S3 uses the [S3A filesystem protocol](https://hadoop.apache.org/docs/current2/hadoop-aws/tools/hadoop-aws/index.html).
After many more hours navigating the netherworld of Hadoop "**JAR hell**", 
I have determined that the following steps are required to successfully 
configure Spark to read from S3.

1. Download [Spark 3.1.1 bundled with Hadoop 3.2](https://spark.apache.org/downloads.html)
2. Download [Hadoop 3.2](https://archive.apache.org/dist/hadoop/common/)
3. Extract both to the local filesystem.
4. Copy the following "fat" JARs from Hadoop to the Spark /jars folder
    - hadoop-3.2.0/share/hadoop/tools/lib/hadoop-aws-3.2.0.jar
    - hadoop-3.2.0/share/hadoop/tools/lib/aws-java-sdk-bundle-1.11.375.jar
5. Build the Spark 3.1.1 container with Python bindings.

# Smoke Tests
- Run SparkPi
```shell
./bin/run-example SparkPi 10
```
- Run pi.py
```shell
./bin/spark-submit examples/src/main/python/pi.py 10
```