#! /usr/bin/env python3

import os
# import mariadb
# import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql:////'
    + os.environ['MYSQL_USER']
    + ':'
    + os.environ['MYSQL_PASSWORD']
    + '@db:3306/matcha')
db = SQLAlchemy(app)
