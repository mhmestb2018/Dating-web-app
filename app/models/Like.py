from app import db


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target = db.relationship('User', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User', backref=db.backref('likes', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name
