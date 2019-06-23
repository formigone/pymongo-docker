#!/bin/sh

PORT=${GUNICORN_PORT:=8080}
CHDIR=${GUNICORN_DIR:='app/api'}

gunicorn api:app --chdir ${CHDIR} -b 0.0.0.0:${PORT}
