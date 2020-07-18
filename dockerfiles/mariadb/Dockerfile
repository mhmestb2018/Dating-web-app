FROM mariadb:latest

COPY matcha.sql /docker-entrypoint-initdb.d/

ENV MYSQL_ROOT_PASSWORD admin
ENV MYSQL_DATABASE matcha
ENV MYSQL_USER admin
ENV MYSQL_PASSWORD admin

EXPOSE 3306