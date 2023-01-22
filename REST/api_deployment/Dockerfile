FROM node:19

WORKDIR /usr/src/app

COPY services ./services/
COPY index.js package.json ./

RUN npm i

EXPOSE 8080

CMD ["node","index.js"]