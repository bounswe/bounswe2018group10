FROM node:latest
WORKDIR /app
ADD package*.json /app/
RUN npm install
ADD . .
RUN npm run build