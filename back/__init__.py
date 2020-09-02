from flask import Flask
from .schema import Schema
import os

config = {
    'host': 'db',
    'port': 3306,
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'database': 'matcha',
}

db = Schema(config)

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.secret_key = os.urandom(12).hex()
    #app.config.from_object(Config)
    app.app_context().push()
    
    return app

