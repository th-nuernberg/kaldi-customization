from ._db import db, AlchemyEncoder
import json


class TrainingResource(db.Model):
    __tablename__ = 'training_resources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    training = db.relationship('Training')
    training_id = db.Column(db.Integer, db.ForeignKey("trainings.id"))

    origin = db.relationship('Resource')
    origin_id = db.Column(db.Integer, db.ForeignKey("resources.id"))

    def __repr__(self):
        return json.dumps(self, cls=AlchemyEncoder)
