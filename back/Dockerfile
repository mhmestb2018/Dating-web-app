FROM python:3.7.8-buster

WORKDIR /app

RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup; chmod +x mariadb_repo_setup; ./mariadb_repo_setup ; apt update; apt install -y libmariadb3 libmariadb-dev

COPY ./requirements.txt /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "gunicorn" ]

CMD ["--bind", "0.0.0.0:5000", "-w", "2", "dating_api.wsgi:create_app()"]
