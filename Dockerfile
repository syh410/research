FROM nvidia/cuda:11.2.2-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Shanghai LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64" CUDA_VISIBLE_DEVICES=0

# RUN echo "deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\n\
# deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse\n\
# deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\n\
# deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse\n\
# deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\n\
# deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse\n\
# deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\n\
# deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse\n\
# deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse\n\
# deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse" > /etc/apt/sources.list

RUN apt update && \
    apt install -y \
        libopencv-dev \
        libsndfile1 \
        python3-pip \
        wget && \
    apt clean autoclean && \
    apt autoremove --yes && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

RUN ln -s /usr/local/cuda-11.2/targets/x86_64-linux/lib/libcublas.so.11 ./usr/local/cuda-11.2/targets/x86_64-linux/lib/libcublas.so && \
    ln -s /usr/local/cuda-11.2/targets/x86_64-linux/lib/libcusolver.so.11 /usr/local/cuda-11.2/targets/x86_64-linux/lib/libcusolver.so && \
    ln -s /usr/lib/x86_64-linux-gnu/libcudnn.so.8 /usr/lib/x86_64-linux-gnu/libcudnn.so

RUN python3 -m pip install pip --upgrade && \
    pip install flask \
        flask-cors \
        grpcio \
        minio \
        paddlehub==2.2.0 \
        paddlespeech && \
    pip install paddlepaddle-gpu==2.2.2.post112 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html

ADD light.pth /root/

RUN hub install pyramidbox_lite_server==1.2.0 && \
    hub install pyramidbox_lite_server_mask==1.3.1 && \
    hub install yolov3_darknet53_pedestrian==1.0.2 && \
    hub install yolov3_darknet53_vehicles==1.0.2

COPY ./app/light_detector/light_YOLOX /root/light_detector/light_YOLOX

RUN cd /root/light_detector/light_YOLOX && \
    pip install -r requirements.txt && \
    pip install -v -e .

COPY ./app /root/

ENTRYPOINT cd /root && python3 server.py
