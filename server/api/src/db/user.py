from ._db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    pw_hash = db.Column(db.String(256))
    salt = db.Column(db.String(64))


    def __repr__(self):
        return '<User #{} (Username: {})>'.format(self.id, self.username)
