from ._db import db, AlchemyEncoder, generate_uuid
import datetime
import enum
import json


class DecodingAudio(db.Model):
    __tablename__ = 'decoding_audios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transcripts = db.Column(db.Text, default='[]')

    audioresource_id = db.Column(db.Integer, db.ForeignKey("audioresources.id"))
    audioresource = db.relationship('AudioResource', uselist=False)

    decoding_id = db.Column(db.Integer, db.ForeignKey("decodings.id"))
    decoding = db.relationship('Decoding', uselist=False)

    callback = db.Column(db.Text, default='{}')

    def __repr__(self):
        return json.dumps(self, cls=AlchemyEncoder)
    