FROM python:3.10-alpine as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

RUN apk add --no-cache gcc libffi-dev g++
WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.2.0

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN . /venv/bin/activate && poetry install --only main

COPY . .
RUN . /venv/bin/activate && poetry build

FROM base as final

RUN apk add --no-cache git

COPY --from=builder /venv /venv
COPY --from=builder /app/dist .
COPY wsgi.ini /app

RUN . /venv/bin/activate && pip install *.whl

ENTRYPOINT ["/venv/bin/uwsgi", "wsgi.ini"]