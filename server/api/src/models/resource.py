from ._db import db, AlchemyEncoder, generate_uuid
import datetime
import enum
import json


class ResourceStateEnum(enum.IntEnum):
    Upload_InProgress = 100
    Upload_Failure = 190

    Preparable = 200
    TextPrep_Enqueued = 210
    TextPrep_InProgress = 220
    TextPrep_Failure = 230

    Trainable = 300

    @staticmethod
    def status_to_string(status):
        return {
            100: 'Upload_InProgress',
            190: 'Upload_Failure',

            200: 'Preparable',
            210: 'TextPrep_Enqueued',
            220: 'TextPrep_InProgress',
            290: 'TextPrep_Failure',

            300: 'Trainable'
            }[status]


class ResourceTypeEnum(enum.IntEnum):
    html = 1
    docx = 2
    txt = 3
    pdf = 4
    png = 5
    jpg = 6

    @staticmethod
    def resource_type_to_string(t):
        return (None, 'html', 'docx', 'txt', 'pdf', 'png', 'jpg')[t]


class Resource(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    uuid = db.Column(db.String(36), name="uuid", primary_key=True, default=generate_uuid)
    upload_date = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow)

    status = db.Column(db.Enum(ResourceStateEnum), default=ResourceStateEnum.Upload_InProgress)
    resource_type = db.Column(db.Enum(ResourceTypeEnum), nullable=True)

    owner_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    owner = db.relationship('User')

    def __repr__(self):
        return json.dumps(self, cls=AlchemyEncoder)

    def has_error(self):
        return self.status == ResourceStateEnum.Upload_Failure \
            or self.status == ResourceStateEnum.TextPrep_Failure

    def mimetype(self):
        return (
            'application/octet-stream',
            'text/html',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain',
            'application/pdf',
            'image/png',
            'image/jpeg')[self.resource_type]
