import os

from .models.schema import Schema

config = {
    'host': 'db',
    'port': 3306,
    'user': os.environ['MYSQL_USER'],
    'password': os.environ['MYSQL_PASSWORD'],
    'database': 'matcha',
}

db = Schema(config)

host = os.environ['REACHABLE_HOST']

mail = None

