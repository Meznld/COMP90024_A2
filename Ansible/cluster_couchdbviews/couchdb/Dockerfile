FROM ubuntu:20.04
FROM python:3.10-bullseye
FROM node:16
FROM debian:9


RUN mkdir /app
WORKDIR /app
COPY package*.json ./
ADD . /app/


RUN apt-get update && apt-get install -y libgeos-dev
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install
RUN apt-get update \
    && apt-get install -y \
    curl \
    gnupg \
    && curl -sL https://deb.nodesource.com/setup_6.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g grunt-cli

CMD python3 database.py
