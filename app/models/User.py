from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile = db.Column(db.Text, unique=True, nullable=True)
    picture_url = db.Column(db.String(2048), unique=True, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.name
