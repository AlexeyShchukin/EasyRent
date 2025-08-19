FROM python:3.11-slim as builder

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

FROM python:3.11-slim

RUN adduser --disabled-password myuser

WORKDIR /app

COPY --from=builder /install /usr/local

COPY core core
COPY src src
COPY templates templates
COPY manage.py manage.py
COPY migrate.sh migrate.sh

RUN chmod +x migrate.sh


#RUN python manage.py collectstatic --noinput

USER myuser

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]