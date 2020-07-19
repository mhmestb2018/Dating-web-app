from sqlalchemy.ext.associationproxy import association_proxy

from app import db

# https://stackoverflow.com/questions/37972778/sqlalchemy-symmetric-many-to-one-friendship


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile = db.Column(db.Text, unique=True, nullable=True)
    picture_url = db.Column(db.String(2048), unique=True, nullable=True)
    sent_likes_rels = db.relationship(
        'Like',
        db.ForeignKey('Like.emitting_user_id'),
        backref='from')
    likes = association_proxy('sent_likes_rels', 'emitting_user_id')

    received_likes_rels = db.relationship(
        'Like',
        db.ForeignKey('Like.receiving_user_id'),
        backref='to')
    liked_by = association_proxy('received_likes_rels', 'receiving_user_id')

    # matches_rels = db.relationship(
    #     'Match',
    #     primaryjoin="or_(User.id==Match.user1_id, "
    #                 "User.id==Match.user2_id)")
    # # To replace by a proper join
    # matches = (association_proxy('matches_rels', 'user1_id')
    #            + association_proxy('matches_rels_2', 'user2_id'))
    matches = db.relationship("Match")

    def __repr__(self):
        return '<User %r>' % self.name


class Like(db.Model):
    __tablename__ = 'likes'
    emmitting_user_id = db.Column(
        db.Integer,
        db.ForeignKey('User.id'),
        primary_key=True)
    receiving_user_id = db.Column(
        db.Integer,
        db.ForeignKey('User.id'),
        primary_key=True)

    def __repr__(self):
        return '<Like from %r>' % self.user.name


class Match(db.Model):
    __tablename__ = 'matches'
    user1_id = db.Column(db.Integer,
                         db.ForeignKey('User.id'),
                         primary_key=True)
    user2_id = db.Column(db.Integer,
                         db.ForeignKey('User.id'),
                         primary_key=True)

    # Implicit one-to-many relations: user1, user2
    # (defined as backrefs in User.)

    def __repr__(self):
        return '<Like from %r>' % self.user.name
