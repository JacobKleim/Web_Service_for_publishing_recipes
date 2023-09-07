# build env
FROM node:13.12.0-alpine as build
WORKDIR /app
COPY package*.json ./
RUN nvm install 14
RUN nvm use 14
COPY . ./
RUN npm run build
CMD cp -r build result_build
