FROM python:3.6.5

MAINTAINER mucheng<leisure_licht@foxmail.com>

ENV PYTHONUNBUFFERED 1

COPY . /app

WORKDIR /app

RUN rm /etc/apt/sources.list && mv ./sources.list /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y --allow-unauthenticated cron=3.0pl1-128ubuntu2 && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

RUN pip install --index-url https://pypi.douban.com/simple --no-cache-dir -r ./deploy/requirements.txt

RUN cp config.ini.example config.ini

