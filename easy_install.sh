#!/bin/bash

# Run in Root

ufw disable

# Install Docker
curl -fsSL get.docker.com -o get-docker.sh
sh get-docker.sh
sleep 2
systemctl enable docker
sleep 2
systemctl start docker
sleep 2

# Build Images
docker build -t tmicm_online .

# Run Container
docker run -d --rm -p 80:8000 tmicm_online
