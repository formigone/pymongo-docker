#!/usr/bin/env bash

PORT=${GUNICORN_PORT:=8008}

gunicorn app.api.api:app -b 0.0.0.0:${PORT}
