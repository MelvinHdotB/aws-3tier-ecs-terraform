#!/usr/bin/env bash
set -e

PORT=8080
lsof -ti tcp:${PORT} | xargs -r kill -9

source .venv/bin/activate
exec uvicorn main:app --reload --host 127.0.0.1 --port ${PORT}