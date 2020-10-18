#import mariadb
from flask import jsonify

from .. import db
from ..utils import Validator

class Tag():
    
    def __init__(self, name):
        self.name = name.lower()
        self.id = Tag.get_id(self.name)
        if not self.id:
            query = """
                INSERT INTO `tags` SET name=?
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

    @staticmethod
    def get_id(name):
        query = """
            SELECT
                id
            FROM tags
            WHERE
                name = ?
            """
        values = db.fetch(query, (name,))
        if len(values) == 0:
            return False
        return values[0][0]
