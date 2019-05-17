from bootstrap import db


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)

    name = db.Column(db.String(50))

    models = db.relationship('Model', backref=db.backref('project', remote_side=[id], lazy=True, cascade='all,delete'))

    def __repr__(self):
        return '<Project #{} (UUID: {})>'.format(self.id, self.uuid)
