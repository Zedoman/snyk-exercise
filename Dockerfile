FROM python:3.14.0a3-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .