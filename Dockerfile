# Dockerfile for Django app using Python 3.10
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set a temporary workdir to install deps
WORKDIR /code

# system deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /code/
RUN pip install --upgrade pip \
    && pip install -r /code/requirements.txt

# Copy project into image
COPY . /code/

# Final workdir where manage.py is located
WORKDIR /code/CesiZen

# Collect static will be run via manage.py or entrypoint

EXPOSE 8000

# Default command: run gunicorn
CMD ["gunicorn", "CesiZen.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
