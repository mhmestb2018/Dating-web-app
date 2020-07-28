from flask import Flask
from app.config import Config
from .models import db



def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)
    app.app_context().push()
    db.init_app(app)

    from . import routes  # Import routes
    #db.create_all()  # Create sql tables for our data models

    return app

