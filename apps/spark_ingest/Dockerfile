# Working pyspark worker container
# FROM bitnami/spark:latest
# USER root
# COPY requirements.txt /opt/spark-ingest/requirements.txt
# RUN pip --no-cache-dir install -r /opt/spark-ingest/requirements.txt \
#     && rm /opt/spark-ingest/requirements.txt
# USER 1001

# Working pyspark client container
FROM openjdk:11-jre-slim
COPY --from=python:3.6.13-slim / /

ENV APP_HOME=/opt/spark-ingest
ENV PATH=$PATH:${APP_HOME}

RUN  useradd -ms /bin/bash -r -d ${APP_HOME} spark-ingest

COPY requirements.txt ${APP_HOME}/requirements.txt

RUN pip install --upgrade pip wheel setuptools \
    && pip --no-cache-dir install -r ${APP_HOME}/requirements.txt \
    && rm /${APP_HOME}/requirements.txt

COPY --chown=spark-ingest:spark-ingest ./ingest ${APP_HOME}/ingest
COPY --chown=spark-ingest:spark-ingest ./main.py ${APP_HOME}

USER spark-ingest

WORKDIR ${APP_HOME}

ENV PYTHONPATH=${APP_HOME}

CMD ["python", "main.py", "--filepath", "./main.py"]