# build env
FROM node:18.16.1-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install 9.5.1
COPY . ./
RUN npm run build
CMD cp -r build result_build
