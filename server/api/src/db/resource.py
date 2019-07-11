from bootstrap import db
import enum

class ResourceStateEnum(enum.IntEnum):
    Upload_InProgress = 0
    Upload_Failure = 1
    TextPreparation_Ready = 9

    TextPreparation_Pending = 10
    TextPreparation_InProgress = 11
    TextPreparation_Failure = 12
    G2P_Ready = 19

    G2P_Pending = 20
    G2P_InProgress = 21
    G2P_Failure = 22
    Train_Ready = 29

    Success = 200

    def status_to_string(status):
        return {
            0: 'Upload_InProgress',
            1: 'Upload_Failure',
            9: 'TextPreparation_Ready',

            10: 'TextPreparation_Pending',
            11: 'TextPreparation_InProgress',
            12: 'TextPreparation_Failure',
            19: 'G2P_Ready',

            20: 'G2P_Pending',
            21: 'G2P_InProgress',
            22: 'G2P_Failure',
            29: 'Train_Ready',

            200: 'Success'}[status]

class ResourceFileTypeEnum(enum.IntEnum):
    html = 1
    docx = 2
    txt = 3
    pdf = 4
    png = 5
    jpg = 6

    def file_type_to_string(t):
        return (None, 'html', 'docx', 'txt', 'pdf', 'png', 'jpg')[t]

class ResourceTypeEnum(enum.IntEnum):
    upload = 1
    prepworker = 2
    g2pworker = 3
    modelresult = 4
    unique_word_list = 5
    corpus = 6

    def type_to_string(t):
        return (None, 'upload', 'prepworker', 'g2pworker', 'modelresult', 'unique_word_list', 'corpus')[t]

class Resource(db.Model):
    __tablename__ = 'resources'

    model_id = db.Column(db.Integer, db.ForeignKey('models.id'), nullable=False, primary_key=True)
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    status = db.Column(db.Enum(ResourceStateEnum))
    resource_type = db.Column(db.Enum(ResourceTypeEnum))

    name = db.Column(db.String(255))
    file_type = db.Column(db.Enum(ResourceFileTypeEnum), nullable=True)

    def __repr__(self):
        if self.resource_type == ResourceTypeEnum.upload:
            return '{{Resource {} "{}"."{}" {}#{} (status: {})}}'.format(
                ResourceTypeEnum.type_to_string(self.resource_type),
                self.name,
                ResourceFileTypeEnum.file_type_to_string(self.file_type),
                self.model_id,
                self.id,
                ResourceStateEnum.status_to_string(self.status))
        else:
            return '{{Resource {} "{}" {}#{} (status: {})}}'.format(
                ResourceTypeEnum.type_to_string(self.resource_type),
                self.name,
                self.model_id,
                self.id,
                ResourceStateEnum.status_to_string(self.status))
