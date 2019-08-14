from ._db import db, AlchemyEncoder, generate_uuid
import datetime
import enum
import json


class DecodingStateEnum(enum.IntEnum):
    Init = 100
    
    Queued = 200

    Decoding_Success = 300
    Decoding_Failure = 320

    @staticmethod
    def status_to_string(status):
        return {
            100: "Init",
            300: "Decoding_Success",
            320: "Decoding_Failure"
        }[status]


class Decoding(db.Model):
    __tablename__ = 'decodings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), name="uuid", primary_key=True, default=generate_uuid)

    training = db.relationship('Training')
    training_id = db.Column(db.Integer,db.ForeignKey("trainings.id"))

    status = db.Column(db.Enum(DecodingStateEnum))
    
    upload_date = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow)

    def __repr__(self):
        return json.dumps(self, cls=AlchemyEncoder)
