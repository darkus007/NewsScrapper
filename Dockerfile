FROM python:3.12.0rc2-alpine3.18

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PATH="/app:$PATH"

WORKDIR /app

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /temp/requirements.txt
RUN pip install --no-cache-dir -r /temp/requirements.txt

COPY . .

RUN python