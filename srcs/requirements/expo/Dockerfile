FROM node:20.7

RUN mkdir -p /app /log

WORKDIR app

RUN npm install -g expo-cli \
	&& expo init --template blank SharePot

COPY ./tools /tmp
