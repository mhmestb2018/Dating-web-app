#import mariadb
from flask import jsonify

from .. import db
from ..utils import Validator

class Tag():
    
    def __init__(self, name):
        self.name = name.lower()
        query = """
            INSERT INTO `tags` SET name=? ON DUPLICATE KEY UPDATE id=id
            """
        self.id = db.exec(query, (Validator.tag(self.name),))

    @staticmethod
    def list(as_user=None):
        query = """
            SELECT DISTINCT
                t.name
            FROM tags t
            INNER JOIN user_tags ut
            ON t.id = ut.tag_id
            """
        params = tuple()
        if as_user is not None:
            query += f"WHERE ut.user_id != ?"
            params = (as_user.id,)
        values = db.fetch(query, params)
        return [row[0] for row in values]
