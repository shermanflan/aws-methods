FROM python:3.9.2-slim

ENV APP_HOME=/opt/async-ingest
ENV PATH=$PATH:${APP_HOME}

RUN  useradd -ms /bin/bash -r -d ${APP_HOME} async-ingest

COPY requirements.txt ${APP_HOME}/requirements.txt

RUN pip3 --no-cache-dir install -r ${APP_HOME}/requirements.txt \
    && rm /${APP_HOME}/requirements.txt

COPY --chown=async-ingest:async-ingest ./ingest ${APP_HOME}/ingest
# COPY --chown=async-ingest:async-ingest ./aws_config ${APP_HOME}/.aws
COPY --chown=async-ingest:async-ingest ./main.py ${APP_HOME}

USER async-ingest

WORKDIR ${APP_HOME}

ENV PYTHONPATH=${APP_HOME}

CMD ["python", "main.py"]