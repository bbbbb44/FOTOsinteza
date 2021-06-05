FROM ubuntu:18.04
WORKDIR /projekt/app
COPY ./projekt/package*.json /projekt/app
RUN apt-get update && apt-get -y install \
vim \
python3 \
python3-numpy \
python3-bs4 \
python3-httplib2 \
python3-requests \
curl
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get update && apt-get -y install nodejs
RUN npm install
RUN npm install express-generator -g
RUN npm install express-mongoose-generator -g
COPY ./projekt /projekt/app
EXPOSE 3000 27017
CMD ["npm", "start"]