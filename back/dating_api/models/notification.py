from flask import jsonify, request
from datetime import datetime
import json

from flask_socketio import send, emit

from .. import db, socketio
from .user import User

class Notification():
    
    def __init__(self, user_id, from_id, notification_type, unread_status=1, date=None):
        self.from_id = from_id
        self.user_id = user_id
        self.type = notification_type
        self.date = date
        self.unread = True if unread_status == 1 else False
        if not self.date:
            query = """
                INSERT INTO notifications SET from_id=?, user_id=?, type=?
                """
            db.exec(query, (from_id, user_id, notification_type,))
            query = """
                SELECT date from notifications WHERE user_id=? AND from_id=? ORDER BY date DESC
                """
            values = db.fetch(query, (user_id, from_id,))
            self.date = values[0][0]
        if type(self.date) is str:
            self.date = datetime.strptime(self.date, "%a, %d %b %Y %H:%M:%S GMT")

    @staticmethod
    def emit_notification(user_id, from_id, notification_type, room):
        notif = Notification(user_id, from_id, notification_type)
        socketio.emit('notification', json.dumps(notif.to_dict), room=room)
        
    @staticmethod
    def read(user_id_1):
        query = """
            UPDATE
                notifications n
            SET
                unread = 0
            WHERE
                n.user_id=?
        """
        rows = db.exec(query, (user_id_1,))
        
    @staticmethod
    def list(user_id_1):
        query = """
            SELECT
                from_id, user_id, type, unread, date
            FROM notifications
            WHERE
                user_id=?
            ORDER BY
                date DESC
            LIMIT 100
            """
        values = db.fetch(query, (user_id_1,))
        return [Notification(*row) for row in values]

    import json
    @property
    def to_dict(self):
        tmp = {
            'from': User.get_user(user_id=self.from_id).intro_as(User.get_user(user_id=self.user_id)),
            'date': self.date.strftime("%Y-%m-%d %H:%M:%S.%f"),
            'type': self.type,
            'unread': self.unread,
        }
        print(tmp)
        return tmp
