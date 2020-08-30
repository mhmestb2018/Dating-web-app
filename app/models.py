import json, mariadb

class Schema:
    def __init__(self, config):
        self.conn = False
        while not self.conn:
            self.conn = mariadb.connect(**config)
        self.cur = self.conn.cursor()
        # Create users first as other tables will refer to it
        self.create_users_table()
        self.populate_users_table()

    def create_users_table(self):

        self.cur.execute("DROP TABLE IF EXISTS users")

        query = """
        CREATE TABLE IF NOT EXISTS users (
        id int NOT NULL AUTO_INCREMENT,
        name varchar(255) NOT NULL,
        picture_url varchar(2083),
        PRIMARY KEY (id)
        );
        """

        self.cur.execute(query)

    def populate_users_table(self):
        query = """
        INSERT INTO users (name, picture_url) VALUES
        ('Toto', 'gjhh'),
        ('Jack', 'gjgh'),
        ('Titi', 'ghgh');
        """
        self.cur.execute(query)

    def exec(self, query):
        if mariadb.mysql_ping(self.conn):
            self.cur.execute(query)
            return True
        return False


class Base():

    pass

class User():
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

    def __init__(self, name, email, bio=""):
        self.name = name
        self.password = ""
        self.picture_url= None
        self.email = email
        self.bio = bio

    def commit(self):
        pass

    def __repr__(self):
        return '<User %r>' % self.name


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
