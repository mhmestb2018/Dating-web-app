FROM python:3.7

WORKDIR /app

COPY ./requirements.txt /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "flask" ]

CMD [ "run", "--host=0.0.0.0" ]