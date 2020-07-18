#! /usr/bin/bash

docker build -t "mariadb" ../mariadb;

docker build -t "flask" ../flask;

docker run --name matcha-db -d -p 3306:3306 mariadb;
export MARIADB_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' matcha-db)

docker run --name matcha-backend -d -p 80:5000 flask -db MARIADB_IP -p 3006