FROM python:3.12-alpine3.17

ENV PYTHONUNBUFFERED True
RUN apk add --no-cache build-base

COPY agents /usr/src/agents
COPY api /usr/src/api
COPY data/csv /usr/src/data/csv
COPY requirements.txt /usr/src
WORKDIR /usr/src

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $PORT

ENTRYPOINT uvicorn --host 0.0.0.0 --port $PORT --workers $WORKERS api.main:app
