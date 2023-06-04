#!/bin/bash

# Install Docker and NVIDIA Container Toolkit
curl https://get.docker.com | sh \
  && sudo systemctl --now enable docker

distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Build Images
#docker build -t tmicm .
#echo "构建成功！"
#docker image ls

# Run Container
docker run -d --network host --gpus all --restart=on-failure ghcr.io/ytawm/tmicm
echo "容器启动成功！"
docker ps -a

# On CPU only
#docker run -d --restart=on-failure \
#  --network host ghcr.dockerproxy.com/ytawm/tmicm \
#  gunicorn --workers=3 --bind :8000 app:app
