FROM node:16-alpine

WORKDIR /app

COPY package*.json /app/
RUN npm install

COPY . /app/

# Exponer el puerto interno
EXPOSE 8080

# Comando por defecto (opcional, ya está en docker-compose)
# CMD ["npm", "run", "serve"]

