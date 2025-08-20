FROM python:3.10-slim-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc wget gnupg gpg-agent \
    && pip install --upgrade pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements/ /app/requirements
RUN pip install -r /app/requirements/production.txt

COPY . /app/

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "6"]
