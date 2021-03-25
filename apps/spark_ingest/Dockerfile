# Working pyspark worker container
# FROM bitnami/spark:latest
# USER root
# COPY requirements.txt /opt/spark-ingest/requirements.txt
# RUN pip --no-cache-dir install -r /opt/spark-ingest/requirements.txt \
#     && rm /opt/spark-ingest/requirements.txt
# USER 1001

# Working pyspark client container
# FROM openjdk:11-jre-slim
# COPY --from=python:3.6.13-slim / /

# Working spark 3.1.1 base container with Python bindings
FROM spark-py:3.1.1

# Reset to root to run installation tasks
USER 0

ENV APP_HOME=${SPARK_HOME}/spark-ingest
ENV PATH=$PATH:${APP_HOME}

COPY requirements.txt ${APP_HOME}/requirements.txt

RUN pip install --upgrade pip wheel setuptools \
    && pip --no-cache-dir install -r ${APP_HOME}/requirements.txt \
    && rm /${APP_HOME}/requirements.txt

COPY ./ingest ${APP_HOME}/ingest
COPY ./main.py ${APP_HOME}
ENV PYTHONPATH=${APP_HOME}

WORKDIR ${SPARK_HOME}/work-dir
ENTRYPOINT [ "/opt/entrypoint.sh" ]

# Specify the User that the actual main process will run as
ARG spark_uid=185
USER ${spark_uid}