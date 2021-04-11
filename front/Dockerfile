FROM node:latest

EXPOSE 3000
COPY ./ /home/node/app
WORKDIR /home/node/app

RUN npm install npm
#RUN npm install -g npm
#RUN npm install react-slider
#RUN npm install --save-dev @types/react-slider
RUN npm install --save react-select
RUN npm install socket.io-client
RUN npm install react-geolocated --save
#RUN npm install react-select --force
RUN npm install
