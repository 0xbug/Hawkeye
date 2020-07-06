FROM python:3.7-stretch
LABEL MAINTAINER=0xbug
ENV TZ=Asia/Shanghai
EXPOSE 80
RUN apt-get update
RUN apt-get install --no-install-recommends -y curl gnupg git redis-server supervisor software-properties-common wget
RUN curl https://openresty.org/package/pubkey.gpg | apt-key add -
RUN add-apt-repository -y "deb http://openresty.org/package/debian stretch openresty"
RUN apt-get update
RUN apt-get install -y openresty
COPY ./deploy /Hawkeye/deploy
RUN pip install --upgrade pip setuptools==45.2.0
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /Hawkeye/deploy/pyenv/requirements.txt -U
RUN cp /Hawkeye/deploy/nginx/*.conf /usr/local/openresty/nginx/conf/
RUN cp /Hawkeye/deploy/supervisor/*.conf /etc/supervisor/conf.d/
COPY ./client/dist /Hawkeye/client/dist
COPY ./server /Hawkeye/server
WORKDIR /Hawkeye/server
COPY ./docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh
CMD ["./docker-entrypoint.sh"]
