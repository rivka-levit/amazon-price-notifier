FROM python:3.12.0-alpine3.18

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app

WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add jpeg-dev zlib-dev libjpeg && \
    apk add bind-tools && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del build-deps && \
    adduser --disabled-password --no-create-home notifier-user

ENV PATH="/py/bin:$PATH"

USER notifier-user
