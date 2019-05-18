from bootstrap import db
import enum


class ResourceStateEnum(enum.IntEnum):
    Upload_InProgress = 0
    Upload_Failure = 1

    TextPreparation_Pending = 10
    TextPreparation_InProgress = 11
    TextPreparation_Failure = 12

    Success = 200


def status_to_string(status):
    return {
        0: 'Upload_InProgress',
        1: 'Upload_Failure',

        10: 'TextPreparation_Pending',
        11: 'TextPreparation_InProgress',
        12: 'TextPreparation_Failure',

        200: 'Success'}[status]


class ResourceTypeEnum(enum.IntEnum):
    HTML = 1
    Word = 2
    Text = 3
    PDF = 4
    PNG = 5
    JPEG = 6


def type_to_string(t):
    return (None, 'HTML', 'Word', 'Text', 'PDF', 'PNG', 'JPEG')[t]


class Resource(db.Model):
    __tablename__ = 'resources'

    model_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=False, primary_key=True)
    id = db.Column(db.Integer, primary_key=True, nullable=True)

    file_name = db.Column(db.String(255))
    file_type = db.Column(db.Enum(ResourceTypeEnum))
    status = db.Column(db.Enum(ResourceStateEnum))

    def __repr__(self):
        return '<Resource "{}" {}#{} (type: {}, status: {}))>'.format(self.file_name, self.model_id, self.id, type_to_string(self.file_type), status_to_string(self.status))
