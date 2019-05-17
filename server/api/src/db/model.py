from bootstrap import db


class Model(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    parent_id = db.Column(db.Integer, db.ForeignKey('models.id'))

    children = db.relationship('Model', backref=db.backref('parent', remote_side=[id], lazy=True))
    resources = db.relationship('Resource', backref=db.backref('model', remote_side=[id], lazy=True, cascade='all,delete'))

    def __repr__(self):
        return '<Model #{} (Project #{})>'.format(self.id, self.project_id)
