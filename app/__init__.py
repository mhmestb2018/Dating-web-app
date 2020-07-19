#! /usr/bin/env python3

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://'
    + os.environ['MYSQL_USER']
    + ':'
    + os.environ['MYSQL_PASSWORD']
    + '@db:3306/matcha')
db = SQLAlchemy(app)
db.create_all()


from app.models import User

me = User(name='john', email='vhjbhb')
db.session.add(me)
db.commit(me)
