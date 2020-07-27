#! /usr/bin/env python3

# import os
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     'mysql+mysqlconnector://'
#     + os.environ['MYSQL_USER']
#     + ':'
#     + os.environ['MYSQL_PASSWORD']
#     + '@db:3306/matcha')
# db = SQLAlchemy(app)
# db.create_all()

from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from app.config import Config


# db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes
        # db.create_all()  # Create sql tables for our data models

        return app

