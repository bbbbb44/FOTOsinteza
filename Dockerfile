FROM ubuntu:18.04
ENV TZ=Europe/Ljubljana
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /projekt/app
COPY ./projekt/package*.json /projekt/app/
RUN apt-get update && apt-get -y install \
vim \
python3 \
mongodb \
python3-pip \
libgl1-mesa-glx \
ffmpeg \
libsm6 \
libxext6 \
curl
RUN pip3 install --upgrade pip
RUN pip3 install numpy \
matplotlib \
opencv-python \
requests \
BeautifulSoup4 \
httplib2 \
tensorflow \
pymongo \
PySide2
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get update && apt-get -y install nodejs
RUN npm install
RUN npm install express-generator -g
RUN npm install express-mongoose-generator -g
COPY ./projekt /projekt/app
EXPOSE 3000 27017