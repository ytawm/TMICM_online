# 基于跨域小样本分类的甲状腺超声图像识别模型与 TMICM 医学图像分类平台

**本项目荣获[第四届江苏省大学生生物医学工程创新设计竞赛](http://bmelm.seu.edu.cn/sy/list.htm)特等奖🏆，荣获命题组—人工智能与生物医学大数据赛题第一名🥇。**

## 模型性能

项目模型在赛方提供的 96 张未标明良恶性测试集中 Accuracy = 95+(1)%, F1-score = 95+(1)%。（由于赛方最终并未告知测试集标签，而在现场通过特定程序对模型结果进行分析，我们仅凭记忆记录下上述结果）。

##  快速部署

推荐通过 TMICM 医学图像分类平台对模型进行测试和使用。

### 最低配置要求

1. 如果您希望通过 GPU 加载模型：

   最低需要 1/20 Nvidia A100，4GB GPU RAM（设备由 [Vultr](www.vultr.com) 提供）或等效的 GPU 性能（单线程）。另外，模型在 GeForce RTX 2080 显卡上运行良好。没有进行其他测试。

2. 如果您希望通过 CPU 加载模型：

   在 CPU - 2核，内存 - 2GB（设备由 [腾讯云](cloud.tencent.com) 提供）机器上可稳定运行三线程。

### 通过 Docker 部署

1. 安装 Docker 和 NVIDIA Container Toolkit（在 CPU 机器上仅安装 Docker 即可）

   ```bash
   # Install Docker and NVIDIA Container Toolkit
   # On Ubuntu or Debian
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
   ```

   

2. 运行容器

   ```bash
   # On GPU
   docker run -d --network host --gpus all --restart=on-failure ghcr.io/ytawm/tmicm
   # On CPU
   docker run -d --restart=on-failure \
     --network host ghcr.dockerproxy.com/ytawm/tmicm \
     gunicorn --workers=3 --bind :8000 app:app
   ```

之后，我们便在 8000 端口成功部署 TMICM 医学图像分类平台。在浏览器打开 [http://localhost:8000](http://localhost:8000) 试试吧！

**在全新的 Ubuntu/Debian 机器上，您也可以通过直接运行 [easy_install.sh](https://github.com/ytawm/TMICM_online/blob/main/easy_install.sh) 一站式快速部署。**

### 手动安装

```bash
# 获得代码
git clone https://github.com/ytawm/TMICM_online.git
cd TMICM_online

# 安装依赖
pip3 install -r requirements.txt

# 运行 TMICM 医学图像分类平台
gunicorn --workers=1 --bind :8000 app:app
```

如果需要测定一组图片或有其他需求，请实例化 [prediction.py](https://github.com/ytawm/TMICM_online/blob/main/prediction.py) 的 Voting 类并调用 Voting.predict(img_path) 方法对图像进行分析。 

## 实现思路及方法

请参考[基于跨域小样本分类的甲状腺超声图像识别模型](https://github.com/ytawm/TMICM_online/blob/main/基于跨域小样本分类的甲状腺超声图像识别模型.pdf)，[答辩 PPT](https://github.com/ytawm/TMICM_online/blob/main/答辩.pptx)。

## 许可

1. 本项目数据集由[第四届江苏省大学生生物医学工程创新设计竞赛](http://bmelm.seu.edu.cn/sy/list.htm)提供。其对数据集要求声明如下：

   ```
   郑重声明：此数据集仅供此次竞赛使用，参赛者不得将参赛作品以及此数据集转让给第三方使用，不得将参赛作品用于任何商业用途及其它使用，比赛完毕自行删除本次赛事相关数据。若违反规定，由此造成的一切后果自负。
   ```

   我们的程序文件夹中已去除赛方提供的数据。我们的模型仅从赛方提供的数据集训练。

2. 本项目除 BIGMS 增强预测算法外代码均以 Mozilla Public License Version 2.0 形式授权。

3. **BIGMS 增强预测算法**相关内容不公开且不允许使用，如需交流请发送 [Issue](https://github.com/ytawm/TMICM_online/issues)。
