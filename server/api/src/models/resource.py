from ._db import db, AlchemyEncoder, generate_uuid
import datetime
import enum
import json


class ResourceStateEnum(enum.IntEnum):
    Upload_InProgress = 0
    Upload_Failure = 1
    TextPreparation_Ready = 9

    TextPreparation_Pending = 10
    TextPreparation_InProgress = 11
    TextPreparation_Failure = 12
    TextPreparation_Success = 13

    @staticmethod
    def status_to_string(status):
        return {
            0: 'Upload_InProgress',
            1: 'Upload_Failure',
            9: 'TextPreparation_Ready',

            10: 'TextPreparation_Pending',
            11: 'TextPreparation_InProgress',
            12: 'TextPreparation_Failure',
            13: 'TextPreparation_Success'
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

    status = db.Column(db.Enum(ResourceStateEnum))
    resource_type = db.Column(db.Enum(ResourceTypeEnum), nullable=True)

    owner_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    owner = db.relationship('User')

    callback = db.Column(db.Text, default='{}')

    def __repr__(self):
        return json.dumps(self, cls=AlchemyEncoder)

    def has_error(self):
        return self.status == ResourceStateEnum.Upload_Failure \
            or self.status == ResourceStateEnum.TextPreparation_Failure

    def mimetype(self):
        return (
            'application/octet-stream',
            'text/html',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain',
            'application/pdf',
            'image/png',
            'image/jpeg')[self.resource_type]
