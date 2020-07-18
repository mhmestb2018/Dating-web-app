FROM python:3.7

#RUN apt-get update -y && \
#    apt-get install -y libmariadb-dev
    # apt-get upgrade -y

WORKDIR /app

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]