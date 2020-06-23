FROM tiangolo/uvicorn-gunicorn-fastapi:python3.6-alpine3.8

ENV PIP_HOST=mirrors.aliyun.com

COPY . /app

RUN set -ex \
    && mkdir -p /var/lib/fish /etc/fish /var/log/fish \
    && cp /app/etc/fish.ini /etc/fish/ \
    && pip3 --trusted-host $PIP_HOST install -i http://$PIP_HOST/pypi/simple --no-cache-dir -r /app/requirements.txt

