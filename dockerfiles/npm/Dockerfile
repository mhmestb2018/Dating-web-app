FROM node:latest

WORKDIR /app
COPY ./front /app
RUN npm install
EXPOSE 3000

# ENTRYPOINT "/bin/bash"
CMD ["npm", "start"]