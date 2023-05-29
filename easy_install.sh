#!/bin/bash

# Run in Root

ufw disable

# Install Nvidia Driver
curl -OL https://nvidia.github.io/nvidia-docker/gpgkey
apt-key add gpgkey
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
apt-get update
apt-get install -y nvidia-container-toolkit

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
echo "构建成功！"
docker image ls

# Run Container
docker run -d --network host --gpus all --restart=on-failure tmicm_online
echo "容器启动成功！"
docker ps -a
