from ._db import db, AlchemyEncoder, generate_uuid
import datetime
import enum
import json


class AudioStateEnum(enum.IntEnum):
    Init = 100
    
    AudioPrep_Pending = 150
    AudioPrep_InProgress = 200

    AudioPrep_Success = 300
    AudioPrep_Failure = 320

    @staticmethod
    def status_to_string(status):
        return {
            100: "Init",
            150: "AudioPrep_Pending",
            200: "AudioPrep_InProgress",
            300: "AudioPrep_Success",
            320: "AudioPrep_Failure"
        }[status]


class AudioResource(db.Model):
    __tablename__ = 'audioresources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), name="uuid", primary_key=True, default=generate_uuid)

    name = db.Column(db.String(256))

    status = db.Column(db.Enum(AudioStateEnum))

    upload_date = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    user = db.relationship('User', uselist=False)

    def __repr__(self):
        return json.dumps(self, cls=AlchemyEncoder)
