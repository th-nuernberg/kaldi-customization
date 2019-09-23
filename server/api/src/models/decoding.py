from ._db import db, AlchemyEncoder, generate_uuid
import datetime
import enum
import json


class DecodingStateEnum(enum.IntEnum):
    Assigned = 100

    Decoding_Enqueued = 110
    Decoding_InProgress = 120
    Decoding_Failure = 190

    Decoded = 200

    @staticmethod
    def status_to_string(status):
        return {
            100: "Assigned",
            110: "Decoding_Enqueued",
            120: "Decoding_InProgress",
            190: "Decoding_Failure",

            200: "Decoded"
        }[status]


class Decoding(db.Model):
    __tablename__ = 'decodings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), name="uuid", primary_key=True, default=generate_uuid)

    training = db.relationship('Training')
    training_id = db.Column(db.Integer,db.ForeignKey("trainings.id"))

    status = db.Column(db.Enum(DecodingStateEnum), default=DecodingStateEnum.Assigned)
    transcripts = db.Column(db.Text, default='[]')

    audio_resource_id = db.Column(db.Integer, db.ForeignKey("audio_resources.id"), nullable=True)
    audio_resource = db.relationship('AudioResource', uselist=False)

    upload_date = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow)

    callback = db.Column(db.String(1024), nullable=True)

    def __repr__(self):
        return json.dumps(self, cls=AlchemyEncoder)
