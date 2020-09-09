import mariadb
from flask import jsonify
from werkzeug.security import check_password_hash

from .. import db
from ..utils import Validator

class User():
    __fields__ = ("id", "first_name", "last_name", "email", "password", "sex", "orientation", "bio", "views_count", "likes_count", "picture_1", "picture_2", "picture_3", "picture_4", "picture_5", "validated")
    __restricted_fields__ = ("id", "validated", "views_count", "likes_count", "id")

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
            print("get_user: missing parameters", flush=True)
            return None

        rows = db.cur.fetchall()
        if len(rows) is 0:
            print("get_user: no results", flush=True)
            return None
        
        values = zip(User.__fields__, rows[0])
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
                    user.score = v / max(tmp, 1E-7)
            else:
                setattr(user, f, v)
        return user

    def __init__(self, user_id=None, first_name=None, last_name=None, email=None, password=None, empty=False):
        self.pictures = []
        self.orientation = None
        self.sex = None
        self.bio = None
        self.score = 0
        self.validated = 0
        if not empty:
            self.first_name = Validator.name(first_name)
            self.last_name = Validator.name(last_name)
            self.email = Validator.email(email)
            self.password = Validator.password(password)
            self.id = user_id

    @staticmethod
    def create_user(first_name, last_name, email, hashed_password):
        # Left to do: send mail

        user = User(db.cur.lastrowid, first_name, last_name, email, hashed_password)
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)"
        db.exec(query, (first_name, last_name, email, hashed_password))
        
        return user

    def update(self, new_values:dict):
        reqs = []
        params = []

        # Unpack pictures array:
        if "pictures" in new_values:
            pictures = new_values["pictures"]
            self.pictures = []
            for i, path in enumerate(pictures):
                path = Validator.path(path)
                setattr(new_values, f"picture_{i}", path)
                self.pictures.append(path)

        for k in new_values.keys():
            if k not in User.__fields__ or k in User.__restricted_fields__:
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

    def delete(self):
        query = "DELETE FROM users WHERE id=" + str(self.id)
        db.exec(query)
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

    def matches(self, user):
        print("in user.matches function", flush=True)
        return True

    def block(self, user):
        query = "INSERT INTO blocks (user_id, blocked) VALUES (?, ?)"
        db.exec(query, (self.id, user.id))
        return True

    def unblock(self, user):
        query = "DELETE FROM blocks WHERE id=" + str(self.id) + " AND liked=" + str(user.id)
        db.exec(query, (self.id, user.id))
        return True

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return self.__str__()

    @property
    def dict(self):
        return vars(self)

    @property
    def public(self):
        return {
            "first_name": self.first_name,
            "id": self.id,
            "pictures": self.pictures,
            "orientation": self.orientation,
            "bio": "",
            "score": self.score,
        }


        
    # __tablename__ = 'users'
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(80), nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=True)
    # bio = db.Column(db.Text, nullable=True)
    # picture_url = db.Column(db.String(2048), unique=True, nullable=True)
    # sent_likes_rels = db.relationship(
    #     'Like',
    #     foreign_keys='Like.emitting_user_id',
    #     primaryjoin='Like.emitting_user_id',
    #     backref='from')
    # likes = association_proxy('sent_likes_rels', 'emitting_user_id')

    # received_likes_rels = db.relationship(
    #     'Like',
    #     foreign_keys='Like.receiving_user_id',
    #     backref='to')
    # liked_by = association_proxy('received_likes_rels', 'receiving_user_id')

    # # matches_rels = db.relationship(
    # #     'Match',
    # #     primaryjoin="or_(User.id==Match.user1_id, "
    # #                 "User.id==Match.user2_id)")
    # # # To replace by a proper join
    # # matches = (association_proxy('matches_rels', 'user1_id')
    # #            + association_proxy('matches_rels_2', 'user2_id'))
    # matches = db.relationship("Match")


# class Like(Base):
#     __tablename__ = 'likes'
#     emitting_user_id = db.Column(
#         db.Integer,
#         foreign_keys='User.id',
#         primary_key=True)
#     receiving_user_id = db.Column(
#         db.Integer,
#         foreign_keys='User.id',
#         primary_key=True)

#     def __repr__(self):
#         return '<Like from %r>' % self.user.name


# class Match(Base):
#     __tablename__ = 'matches'
#     user1_id = db.Column(db.Integer,
#                          db.ForeignKey('User.id'),
#                          primary_key=True)
#     user2_id = db.Column(db.Integer,
#                          db.ForeignKey('User.id'),
#                          primary_key=True)

#     # Implicit one-to-many relations: user1, user2
#     # (defined as backrefs in User.)

#     def __repr__(self):
#         return '<Like from %r>' % self.user.name
