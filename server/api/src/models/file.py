from ._db import db
import enum

class FileStateEnum(enum.IntEnum):
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

class FileTypeEnum(enum.IntEnum):
    html = 1
    docx = 2
    txt = 3
    pdf = 4
    png = 5
    jpg = 6

    @staticmethod
    def file_type_to_string(t):
        return (None, 'html', 'docx', 'txt', 'pdf', 'png', 'jpg')[t]


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    status = db.Column(db.Enum(FileStateEnum))
    file_type = db.Column(db.Enum(FileTypeEnum), nullable=True)

    owner_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    owner = db.relationship('User')

    def __repr__(self):
        return "File"
