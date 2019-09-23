from ._db import db, AlchemyEncoder, generate_uuid
import datetime
import enum
import json


class AudioStateEnum(enum.IntEnum):
    Upload_InProgress = 100
    Upload_Failure = 190

    Preparable = 200
    AudioPrep_Enqueued = 210
    AudioPrep_InProgress = 220
    AudioPrep_Failure = 290

    Decodable = 300

    @staticmethod
    def status_to_string(status):
        return {
            100: 'Upload_InProgress',
            190: 'Upload_Failure',

            200: 'Preparable',
            210: 'AudioPrep_Enqueued',
            220: 'AudioPrep_InProgress',
            290: 'AudioPrep_Failure',
            300: 'Decodable'
        }[status]


class AudioResource(db.Model):
    __tablename__ = 'audio_resources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), name="uuid", primary_key=True, default=generate_uuid)

    name = db.Column(db.String(256))

    status = db.Column(db.Enum(AudioStateEnum))

    upload_date = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    owner = db.relationship('User', uselist=False)

    def __repr__(self):
        return json.dumps(self, cls=AlchemyEncoder)
