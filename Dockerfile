FROM python:3.12.0b4-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .