from ._db import db
import enum


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    uuid = db.Column(db.String(32))

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner = db.relationship('User')

    acoustic_model_id = db.Column(db.Integer, db.ForeignKey("acousticmodels.id"))
    acoustic_model = db.relationship('AcousticModel')

    parent_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=True)
    parent = db.relationship('Project')

    create_date = db.Column(db.DateTime(timezone=False))


    def __repr__(self):
        return '<Project #{} (UUID: {})>'.format(self.id, self.uuid)
