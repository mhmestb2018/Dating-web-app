import json, mariadb

from .. import db

class User():
    __fields__ = ("id", "first_name", "last_name", "email", "password", "sex", "orientation", "bio", "views_count", "likes_count", "main_picture", "validated")
    __restricted_fields__ = ("id", "validated")

    @staticmethod
    def get_user(**kwargs):
        if "email" in kwargs:
            print(f"\tEMAIL: {kwargs['email']}", flush=True)
            query = "SELECT * FROM users WHERE email=?"
            db.exec(query,  (kwargs['email'],))
        elif "user_id" in kwargs:
            query = "SELECT * FROM users WHERE id=?"
            db.exec(query,  (kwargs['user_id'],))
        else:
            return json.dumps({"error": "La recherche d'utilisateur demande un email ou un user_id en paramètre"})

        rows = db.cur.fetchall()
        if len(rows) is 0:
            return False
        values = zip(User.__fields__, rows[0])
        user = User()
        for f, v in values:
            setattr(user, f, v)
        return user

    def __init__(self, user_id=None, first_name=None, last_name=None, email=None, password=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.id = user_id

    @staticmethod
    def create_user(first_name, last_name, email, hashed_password):
        # Left to do: send mail

        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)"
        db.exec(query, (first_name, last_name, email, hashed_password))
        
        return User(db.cur.lastrowid, first_name, last_name, email, hashed_password)

    def update(self, new_values:dict):
        reqs = []
        params = []
        for k in new_values.keys():
            if k not in User.__fields__ or k in User.__restricted_fields__:
                raise Exception(f"field {k} doesn't exist")
            reqs += [f"{k}=?"]
        req = ", ".join(reqs)
        query = "UPDATE users SET " + req + " WHERE id=" + str(self.id)
        db.exec(query, tuple(new_values.values()))
        for (k, v) in new_values.items():
            setattr(self, k, v)
        return True

    def delete(self):
        query = "DELETE FROM users WHERE id=" + str(self.id)
        db.exec(query)
        return True

    def __str__(self):
        return self.to_JSON()

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return vars(self)

    def to_JSON(self):
        return json.dumps(self.to_dict())

    @property
    def public(self):
        return {
            "first_name": self.first_name,
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
