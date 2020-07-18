#! /usr/bin/env python3

import os
import mariadb
import json
from flask import Flask


app = Flask(__name__)

# configuration used to connect to MariaDB
config = {
    'host': 'db',
    'port': 3306,
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'database': 'matcha',
}


@app.route("/")
def Coucou():
    return "Coucou moi"

@app.route("/route")
def CoucouRoute():
    return "Encore moi"

@app.route("/users/<user>")
def user_page(user):
    return "Coucou " + user

@app.route("/dbtest")
def dbtest():
    # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    # execute a SQL statement
    cur.execute("select * from users")
    # get headers
    header = [item[0] for item in cur.description]
    # get all matches
    res = cur.fetchall()
    # jsonify
    json_data=[]
    for item in res:
        json_data.append(dict(zip(header,item)))
    # DUMP !
    return json.dumps(json_data)


if __name__ == "__main__":
    app.run() 