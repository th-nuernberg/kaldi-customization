from ._db import db, AlchemyEncoder, generate_uuid
import enum
import json

class ModelType(enum.IntEnum):
    HMM_GMM = 100
    HMM_DNN = 200
    HMM_RNN = 300


    def type_to_string(status):
        return {
            100: "HMM_GMM",
            200: "HMM_DNN",
            300: "HMM_RNN"
            }[status]

class AcousticModel(db.Model):
    __tablename__ = 'acousticmodels'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    uuid = db.Column(db.String(36), name="uuid", primary_key=True, default=generate_uuid)

    language = db.relationship('Language')#, backref=db.backref('project', remote_side=[id], lazy=True, cascade='all,delete'))
    language_id = db.Column(db.Integer,db.ForeignKey("languages.id"))
    model_type = db.Column(db.Enum(ModelType), nullable=True)

    def __repr__(self):
        return json.dumps(self, cls=AlchemyEncoder)
        