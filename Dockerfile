FROM python:3.6.6-alpine3.8
MAINTAINER eshujiushiwo <liyang@teambition.com>

# application folder
ENV APP_DIR /app/Hawkeye
COPY ./ /app/Hawkeye

WORKDIR ${APP_DIR}

# cron auto create crontab rule using /app/Hawkeye/venv/bin/python so we create soft link for it
RUN echo "http://mirrors.aliyun.com/alpine/latest-stable/main/" > /etc/apk/repositories && \
    apk add musl-dev libxslt-dev  py3-lxml python3-dev libxml2 libxslt libxslt-dev libxml2-dev    gcc bash libffi-dev openssl-dev linux-headers build-base &&\
    pip install -r /app/Hawkeye/deploy/requirements.txt &&\
    mkdir -p /app/Hawkeye/venv/bin/ &&\
    ln -s /usr/local/bin/python /app/Hawkeye/venv/bin/python &&\
    chmod +x entrypoint.sh

EXPOSE 5000
CMD ["./entrypoint.sh"]
