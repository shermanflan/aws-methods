FROM python:3.9.2-slim

ENV APP_HOME=/opt/spark-ingest
ENV PATH=$PATH:${APP_HOME}

RUN  useradd -ms /bin/bash -r -d ${APP_HOME} spark-ingest

COPY requirements.txt ${APP_HOME}/requirements.txt

RUN pip3 --no-cache-dir install -r ${APP_HOME}/requirements.txt \
    && rm /${APP_HOME}/requirements.txt

COPY --chown=spark-ingest:spark-ingest ./ingest ${APP_HOME}/ingest
COPY --chown=spark-ingest:spark-ingest ./main.py ${APP_HOME}

USER spark-ingest

WORKDIR ${APP_HOME}

ENV PYTHONPATH=${APP_HOME}

CMD ["python", "main.py"]