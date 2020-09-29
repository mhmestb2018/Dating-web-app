import mariadb
from flask import jsonify
from werkzeug.security import check_password_hash

from .. import db
from ..utils import Validator

class User():
    __fields__ = ("id", "first_name", "last_name", "email", "password", "sex", "orientation", "bio", "views_count", "likes_count", "picture_1", "picture_2", "picture_3", "picture_4", "picture_5", "validated")
    __restricted_fields__ = ("id", "validated", "views_count", "likes_count", "id")

    def list_users(self):
        query = """
            SELECT
                *
            FROM
                users
                LEFT OUTER JOIN (likes a
                    INNER JOIN likes b
                        ON a.user_id = b.liked
                        AND a.liked = b.user_id
                        AND b.user_id=?)
                    ON users.id = a.user_id
                LEFT OUTER JOIN blocks
                    ON users.id = blocks.user_id
                    AND blocks.blocked=?
            WHERE
                blocks.user_id IS NULL
                AND b.user_id IS NULL
                AND users.validated=1
                AND users.id != ?
            """
        db.exec(query, (self.id, self.id, self.id))

        rows = db.cur.fetchall()
        return [User.build_from_db_tuple(t).public_as(self) for t in rows]

    # def list_users(self):
    #     query = """
    #         SELECT
    #             u.*
    #         FROM
    #             users u
    #             LEFT JOIN (likes a
    #                 INNER JOIN likes b
    #                     ON a.user_id = b.liked
    #                     AND a.liked = b.user_id
    #                     AND b.user_id=?)
    #                 ON a.user_id = u.id
    #         WHERE
    #             b.user_id IS NULL
    #             AND u.validated=1
    #             AND u.id != ?
    #         """
    #     db.exec(query, (self.id, self.id))

    #     rows = db.cur.fetchall()
    #     return [User.build_from_db_tuple(t) for t in rows]

    @staticmethod
    def build_from_db_tuple(values):
        values = zip(User.__fields__, values)
        user = User(empty=True)
        for f, v in values:
            if "picture" in f:
                if v:
                    user.pictures.append(v)
            elif "count" in f:
                tmp = None
                if "views" in f:
                    tmp = v
                elif "likes" in f and tmp is not None:
                    user.score = float(v) / max(tmp, 1E-7)
            else:
                setattr(user, f, v)
        return user

    @staticmethod
    def get_user(**kwargs):
        if "email" in kwargs:
            email = Validator.email(kwargs['email'])
            query = "SELECT * FROM users WHERE email=?"
            db.exec(query,  (email,))
        elif "user_id" in kwargs:
            query = "SELECT * FROM users WHERE id=?"
            db.exec(query,  (kwargs['user_id'],))
        else:
            #print("get_user: missing parameters", flush=True)
            return None

        rows = db.cur.fetchall()
        if len(rows) is 0:
            #print("get_user: no results", flush=True)
            return None
    
        return User.build_from_db_tuple(rows[0])

    def __init__(self, user_id=None, first_name=None, last_name=None, email=None, password=None, empty=False):
        self.pictures = []
        self.orientation = None
        self.sex = None
        self.bio = None
        self.score = 0.0
        self.validated = 0
        if not empty:
            self.first_name = Validator.name(first_name)
            self.last_name = Validator.name(last_name)
            self.email = Validator.email(email)
            self.password = Validator.password(password)
            self.id = user_id

    @staticmethod
    def create_user(first_name, last_name, email, hashed_password, validation_id):

        user = User(0, first_name, last_name, email, hashed_password)
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)"
        db.exec(query, (first_name, last_name, email, hashed_password))
        user.id = db.cur.lastrowid

        query = "INSERT INTO validations (user_id, validation_id) VALUES (?, ?)"
        db.exec(query, (user.id, validation_id))

        return user

    def update(self, new_values:dict, force=False):
        reqs = []
        params = []

        new_values = dict(new_values)
        # Unpack pictures array:
        if "pictures" in new_values:
            pictures = []
            import json
            print(new_values["pictures"])
            pictures += new_values["pictures"]
            print(pictures, flush=True)
            self.pictures = []
            for i, path in enumerate(pictures):
                path = Validator.path(path)
                new_values[f"picture_{i+1}"] = path
                self.pictures.append(path)
            del new_values["pictures"]

        for k in new_values.keys():
            if k not in User.__fields__ or (k in User.__restricted_fields__ and not force):
                raise Exception(f"field {k} doesn't exist")
            reqs += [f"{k}=?"]
        req = ", ".join(reqs)
        query = "UPDATE users SET " + req + " WHERE id=" + str(self.id)
        for (k, v) in new_values.items():
            if "picture" in k:
                continue
            checker = getattr(Validator, k)
            setattr(self, k, checker(v))
        db.exec(query, tuple(new_values.values()))
        return True

    @staticmethod
    def validate(validation_id):
        query = """
            SELECT
                u.*
            FROM users u
                INNER JOIN validations v
                    ON v.user_id = u.id
                    AND v.validation_id = ?
            """
        db.exec(query, (validation_id,))
        rows = db.cur.fetchall()
        if len(rows) is 0:
            return False
        db.exec("UPDATE users SET validated=1 WHERE id=?", (rows[0][0],))
        db.exec("DELETE FROM validations WHERE user_id=?", (rows[0][0],))
        return True

    def delete(self):
        query = "DELETE FROM likes WHERE user_id=? OR liked=?"
        db.exec(query, (self.id, self.id))
        query = "DELETE FROM blocks WHERE user_id=? OR blocked=?"
        db.exec(query, (self.id, self.id))
        query = "DELETE FROM users WHERE id=" + str(self.id)
        db.exec(query)
        self.clear_resets()
        self.clear_blocks()
        self.clear_likes()
        return True

    def like(self, user):
        query = "SELECT * FROM likes WHERE user_id=? AND liked=?"
        db.exec(query, (self.id, user.id))

        rows = db.cur.fetchall()
        if len(rows) is not 0:
            return False
        query = "INSERT INTO likes (user_id, liked) VALUES (?, ?)"
        db.exec(query, (self.id, user.id))
        return True

    def unlike(self, user):
        query = "SELECT * FROM likes WHERE user_id=? AND liked=?"
        db.exec(query, (self.id, user.id))

        rows = db.cur.fetchall()
        if len(rows) is 0:
            return False
        query = "DELETE FROM likes WHERE user_id=? AND liked=?"
        db.exec(query, (self.id, user.id))
        return True

    def liked(self, user):
        query = "SELECT * FROM likes WHERE user_id=? AND liked=?"
        db.exec(query, (self.id, user.id))
        like = db.cur.fetchall()
        if len(like) is 0:
            return False
        return True

    def matches_with(self, user):
        if self.liked(user) and user.liked(self):
            return True
        return False

    def block(self, user):
        query = "SELECT * FROM blocks WHERE user_id=? AND blocked=?"
        db.exec(query, (self.id, user.id))

        rows = db.cur.fetchall()
        if len(rows) is not 0:
            return False
        query = "INSERT INTO blocks (user_id, blocked) VALUES (?, ?)"
        db.exec(query, (self.id, user.id))
        return True

    def unblock(self, user):
        query = "SELECT * FROM blocks WHERE user_id=? AND blocked=?"
        db.exec(query, (self.id, user.id))

        rows = db.cur.fetchall()
        if len(rows) is 0:
            return False
        query = "DELETE FROM blocks WHERE user_id=? AND blocked=?"
        db.exec(query, (self.id, user.id))
        return True

    @property
    def blocklist(self):
        query = "SELECT blocked FROM blocks WHERE user_id=?"
        db.exec(query, (self.id,))

        return [int(i[0]) for i in db.cur.fetchall()]
    
    @property
    def matchlist(self):
        query = """
            SELECT
                u.*
            FROM users u
            INNER JOIN(likes a
                INNER JOIN likes b
                    ON a.user_id = b.liked
                    AND a.liked = b.user_id
                    AND b.user_id = ?)
                ON
                    u.id = a.user_id
            """
        db.exec(query, (self.id,))

        rows = db.cur.fetchall()
        return [User.build_from_db_tuple(t).public_as(self) for t in rows]

    @property
    def blocked_by(self):
        query = "SELECT user_id FROM blocks WHERE blocked=?"
        db.exec(query, (self.id,))

        return [int(i[0]) for i in db.cur.fetchall()]

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return self.__str__()

    @property
    def dict(self):
        d = vars(self)
        return d

    def public_as(self, user):
        d = self.public
        d["liked"] = user.liked(self)
        d["matches"] = user.matches_with(self)
        d["blocked"] = self.id in user.blocklist 
        return d

    @property
    def public(self):
        return {
            "first_name": self.first_name,
            "id": self.id,
            "pictures": self.pictures,
            "orientation": self.orientation,
            "bio": "",
            "score": self.score,
            "sex": self.sex
        }

    def save_reset_id(self, reset_id):
        query = "INSERT INTO resets (user_id, reset_id) VALUES (?, ?)"
        db.exec(query, (self.id, reset_id))

    @property
    def reset_id(self):
        query = "SELECT reset_id FROM resets WHERE user_id=?"
        db.exec(query, (self.id,))

        rows = db.cur.fetchall()
        if len(rows) is 0:
            return False
        return rows[0]

    def clear_resets(self):
        query = "DELETE from resets WHERE user_id=?"
        db.exec(query, (self.id,))

    def clear_blocks(self):
        query = "DELETE from blocks WHERE user_id=? or blocked=?"
        db.exec(query, (self.id, self.id))

    def clear_likes(self):
        query = "DELETE from likes WHERE user_id=? or liked=?"
        db.exec(query, (self.id, self.id))
        