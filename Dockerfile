FROM python:3.7
LABEL MAINTAINER=0xbug
ENV TZ=Asia/Shanghai
EXPOSE 80
COPY ./deploy/apt/sources.list /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y wget gnupg curl redis-server
RUN curl https://openresty.org/package/pubkey.gpg | apt-key add -
RUN apt-get -y install software-properties-common
RUN add-apt-repository -y "deb http://openresty.org/package/debian $(lsb_release -sc) openresty"
RUN apt-get update
RUN apt-get install -y openresty supervisor git
RUN mkdir -p /root/.pip
ADD ./deploy /Hawkeye/deploy
RUN cp /Hawkeye/deploy/pyenv/*.conf /root/.pip/
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /Hawkeye/deploy/pyenv/requirements.txt -U
RUN cp /Hawkeye/deploy/nginx/*.conf /usr/local/openresty/nginx/conf/
RUN cp /Hawkeye/deploy/supervisor/*.conf /etc/supervisor/conf.d/
ADD ./client/dist /Hawkeye/client/dist
ADD ./server /Hawkeye/server
WORKDIR /Hawkeye/server
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]