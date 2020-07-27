"""Flask configuration variables."""
from os import environ#, path
from datetime import timedelta

# # to set Flask configuration from .env file:
# from dotenv import load_dotenv
# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from .env file."""

    # General Config

    # Needed to encrypt/decrypt session data
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    #FLASK_ENV = environ.get('FLASK_ENV')
    PERMANENT_SESSION_LIFETIME = timedelta(days=5)

    # Database
    SQLALCHEMY_DATABASE_URI = (
        'mysql+mysqlconnector://'
        + environ.get('MYSQL_USER')
        + ':'
        + environ.get('MYSQL_PASSWORD')
        + '@db:3306/matcha')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False