FROM node:20.7

RUN mkdir -p /log

WORKDIR /app

RUN npm install -g expo-cli \
	&& expo init --template blank SharePot

RUN npm install react-router-dom

COPY ./tools /tmp
