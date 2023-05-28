# TMICM_online Docker Image
# https://github.com/ytawm/TMICM_online
# Copyright (c) 2022 Metaphorme <https://github.com/Metaphorme>


FROM ubuntu:20.04 as builder
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

FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu20.04
COPY --from=builder /Python-3.11.3 /tmp/Python-3.11.3
COPY *.py *.txt /app/
COPY models /app/models
COPY static /app/static
COPY templates /app/templates

# Install Python packages
RUN /bin/bash -c " \
    set -ex \
    && apt-get update; apt-get install -y make libglvnd-dev libglib2.0-0 \
    && cd /tmp/Python-3.11.3 \
    && make install \
    && cd /app \
    && pip3 install --upgrade pip \
    && pip3 install -r requirements.txt \
    && mkdir tmp \
    "

EXPOSE 8000
WORKDIR /app

CMD [ "gunicorn", "--workers=4", "app:app" ]
