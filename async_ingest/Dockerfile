# 20.04 supports msodbcsql17
FROM ubuntu:20.04

ENV APP_HOME=/opt/async-ingest
ENV PATH=$PATH:${APP_HOME}

RUN  useradd -ms /bin/bash -r -d ${APP_HOME} async-ingest

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York

ARG ODBC_DRIVER_URI=https://s3.amazonaws.com/redshift-downloads/drivers/odbc/1.4.20.1001/AmazonRedshiftODBC-64-bit-1.4.20.1001-1.x86_64.deb
ARG ODBC_DRIVER=AmazonRedshiftODBC-64-bit-1.4.20.1001-1.x86_64.deb

RUN apt-get update \
    && apt-get install -y \
        wget \ 
        # curl git \
        build-essential \
        software-properties-common \
    && apt-get update \
    && wget ${ODBC_DRIVER_URI} \
    && apt-get install ./${ODBC_DRIVER} \
    && apt-get install -y \
        # For parquet, snappy
        llvm libsnappy-dev \
        python3-pip \
        # For psycopg2
        python3-dev libpq-dev \
        python-setuptools \
    && apt-get purge -y software-properties-common \
    # && apt-get purge -y curl git software-properties-common \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ${APP_HOME}/requirements.txt

RUN pip3 --no-cache-dir install -r ${APP_HOME}/requirements.txt \
    && rm /${APP_HOME}/requirements.txt \
    && apt-get purge -y build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=async-ingest:async-ingest ./ingest ${APP_HOME}/ingest
COPY --chown=async-ingest:async-ingest ./main.py ${APP_HOME}

USER async-ingest

WORKDIR ${APP_HOME}

ENV PYTHONPATH=${APP_HOME}

CMD ["python3", "main.py"]