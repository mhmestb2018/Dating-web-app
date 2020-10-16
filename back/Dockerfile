FROM python:3.7

WORKDIR /app

COPY ./requirements.txt /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "gunicorn" ]

CMD ["--bind", "0.0.0.0:5000", "-w", "2", "dating_api.wsgi:create_app()"]