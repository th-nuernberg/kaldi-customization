from ._db import db, AlchemyEncoder
import enum
import datetime
import json


class TrainingStateEnum(enum.IntEnum):
    ###############################################

    # empty training
    Empty = 100

    # waiting for text prep processing assigned resources
    TextPrep_Pending = 110
    # text prep reported failure for already assigned resource
    TextPrep_Failure = 190

    # resources assigned and resource state is TextPrep_Success
    Preparable = 200

    ###############################################
    # Data Prep

    # task in data prep queue, but not processed by data prep worker
    DataPrep_Enqueue = 210
    # status queue update by data prep worker
    DataPrep_InProgress = 220

    DataPrep_Failure = 290

    # training can be started
    Trainable = 300

    # Data Prep
    ###############################################
    # Kaldi

    # task in kaldi queue, but not processed by kaldi worker
    Training_Enqueue = 310
    # status queue update by kaldi worker (start processing)
    Training_In_Progress = 320

    Training_Failure = 390

    # training finished
    Decodable = 400

    # Kaldi
    ###############################################

    @staticmethod
    def status_to_string(status):
        return {
            100: "Empty",
            110: "TextPrep_Pending",

            190: "TextPrep_Failure",
            200: "Preparable",

            210: "DataPrep_Enqueued",
            220: "DataPrep_InProgress",

            290: "DataPrep_Failure",
            300: "Trainable",

            310: "Training_Enqueued",
            320: "Training_InProgress",

            390: "Training_Failure",
            400: "Decodable",
        }[status]


class Training(db.Model):
    __tablename__ = 'trainings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    project = db.relationship('Project')
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    version = db.Column(db.Integer, autoincrement=True)

    create_date = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow)
    status = db.Column(db.Enum(TrainingStateEnum), default=TrainingStateEnum.Empty)

    callback = db.Column(db.String(1024), nullable=True)

    def can_assign_resource(self):
        return self.status in (TrainingStateEnum.Empty,
                               TrainingStateEnum.TextPrep_Pending,
                               TrainingStateEnum.TextPrep_Failure,
                               TrainingStateEnum.Preparable)

    def can_edit(self):
        return self.status in (DB_TrainingStateEnum.Empty,
                               DB_TrainingStateEnum.TextPrep_Pending,
                               DB_TrainingStateEnum.TextPrep_Failure,
                               DB_TrainingStateEnum.Preparable)

    def __repr__(self):
        return json.dumps(self, cls=AlchemyEncoder)
