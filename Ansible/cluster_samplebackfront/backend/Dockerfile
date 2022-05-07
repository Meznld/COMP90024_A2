FROM ubuntu:20.04
FROM python:3.10-bullseye

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD python /app/app.py
