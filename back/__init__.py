from flask import Flask
from flask_mail import Mail
import os

from .schema import Schema

config = {
    'host': 'db',
    'port': 3306,
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'database': 'matcha',
}

db = Schema(config)

host = os.environ['REACHABLE_HOST']

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.secret_key = os.urandom(12).hex()
    
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.environ['FLASK_GMAIL']
    app.config['MAIL_PASSWORD'] = os.environ['FLASK_GMAIL_PASSWORD']
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    print(os.environ['FLASK_GMAIL'], flush=True)
    if os.environ['FLASK_GMAIL'] is "":
        mail = False
    else:
        mail = Mail(app)

    app.app_context().push()    
    return app, mail

