from ._db import db, AlchemyEncoder, generate_uuid
import enum
import datetime
import json

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    uuid = db.Column(db.String(36), name="uuid", primary_key=True, default=generate_uuid)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner = db.relationship('User')

    acoustic_model_id = db.Column(db.Integer, db.ForeignKey("acoustic_models.id"))
    acoustic_model = db.relationship('AcousticModel')

    parent_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=True)
    parent = db.relationship('Project', uselist=False)

    create_date = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow)

    #TODO Trainings?

    def __repr__(self):
        return json.dumps(self, cls=AlchemyEncoder)
