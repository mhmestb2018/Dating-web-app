#! /usr/bin/env python3

import json
from app import app

# configuration used to connect to MariaDB


@app.route("/")
def Coucou():
    return "Coucou moi"


@app.route("/route")
def CoucouRoute():
    return app.config['SQLALCHEMY_DATABASE_URI']


@app.route("/users/<user>")
def user_page(user):
    return "Coucou " + user


@app.route("/dbtest")
def dbtest():
    import os
    import mariadb
    config = {
        'host': 'db',
        'port': 3306,
        'user': os.environ['MYSQL_USER'],
        'password': os.environ['MYSQL_PASSWORD'],
        'database': 'matcha',
    }

    # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    # execute a SQL statement
    cur.execute("select * from user")
    # get headers
    header = [item[0] for item in cur.description]
    # get all matches
    res = cur.fetchall()
    # jsonify
    json_data = []
    for item in res:
        json_data.append(dict(zip(header, item)))
    # DUMP !
    return json.dumps(json_data)
