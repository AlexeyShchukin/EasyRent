FROM python:3.13-slim as builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --prefix=/install -r requirements.txt gunicorn

FROM python:3.13-slim

RUN adduser --disabled-password myuser

WORKDIR /app

COPY --from=builder /install /usr/local

COPY core core
COPY src src
COPY manage.py manage.py

USER root

EXPOSE 8000