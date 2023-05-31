#!/usr/bin/env bash

# Install Docker
curl -fsSL get.docker.com -o get-docker.sh
sh get-docker.sh
sleep 2
systemctl enable docker
sleep 2
systemctl start docker
sleep 2

# Run Docker image
docker run -d \
   --name tmicm \
   -v $(pwd):/usr/local/etc/haproxy:ro \
   -p 80:80 \
   -p 443:443 \
   -p 8404:8404 \
   haproxytech/haproxy-alpine:latest
