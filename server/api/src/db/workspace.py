from bootstrap import db


class Workspace(db.Model):
    __tablename__ = 'workspaces'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)

    name = db.Column(db.String(50))

    projects = db.relationship('Project', backref=db.backref('workspace', remote_side=[id], lazy=True, cascade='all,delete'))

    # TODO: members

    def __repr__(self):
        return '<Project #{} (UUID: {})>'.format(self.id, self.uuid)
