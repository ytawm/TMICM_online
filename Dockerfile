# TMICM_online Docker Image
# https://github.com/ytawm/TMICM_online
# Copyright (c) 2022 Metaphorme <https://github.com/Metaphorme>
# 用于快速部署单个节点的 TMICM 在线服务


FROM ubuntu:22.04 as builder
ARG DEBIAN_FRONTEND=noninteractive

# Build Python
RUN /bin/bash -c " \
    set -ex \
    && apt-get update; apt-get install -y build-essential gdb lcov pkg-config \
      libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
      libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev curl \
      lzma lzma-dev tk-dev uuid-dev zlib1g-dev \
    && curl -SL https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz | tar -xzC . ; cd Python-3.11.3 \
    && ./configure --enable-optimizations --prefix=/usr/local && make -j4 \
    "

FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu22.04
COPY --from=builder /Python-3.11.3 /tmp/Python-3.11.3
COPY *.py *.txt /app/
COPY models /app/models
COPY static /app/static
COPY templates /app/templates

# Install Python packages
RUN /bin/bash -c " \
    set -ex \
    && apt-get update; apt-get install -y make libglvnd-dev libglib2.0-0 curl \
    && cd /tmp/Python-3.11.3 \
    && make install \
    && cd /app; rm -rf /tmp/Python-3.11.3 \
    && pip3 install -r requirements.txt \
    && mkdir tmp \
    "

EXPOSE 8000
WORKDIR /app

CMD [ "gunicorn", "--workers=1", "--bind", ":8000", "app:app" ]

HEALTHCHECK --interval=60s --timeout=3s \
  CMD curl -fs http://localhost:8000/ || exit 1
