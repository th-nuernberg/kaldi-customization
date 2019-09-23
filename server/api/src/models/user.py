from ._db import db
from passlib.hash import sha256_crypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(256))


    def check_password(self, password):
        return sha256_crypt.verify(password, self.password)

    def get_user_id(self):
        return self.id

    def __repr__(self):
        return '<User #{} (Username: {})>'.format(self.id, self.username)
