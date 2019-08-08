from ._db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    user_email = db.Column(db.String(255))
    pw_hash = db.Column(db.String(256))
    salt = db.Column(db.String(64))


    def check_password(self, password):
        return password == 'valid'

    def get_user_id(self):
        return self.id

    def __repr__(self):
        return '<User #{} (Username: {})>'.format(self.id, self.username)
