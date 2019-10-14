from ._db import db, AlchemyEncoder
import enum
import datetime
import json


class TrainingStateEnum(enum.IntEnum):
    ###############################################

    # empty training
    Init = 100

    # waiting for test prep processing assigned resources
    TextPrep_Pending = 150
    # text prep reported failure for already assigned resource
    TextPrep_Failure = 151

    # resources assigned and resource state is TextPreparation_Success
    Trainable = 200

    ###############################################
    # Data Prep

    # task in data prep queue, but not processed by data prep worker
    Training_DataPrep_Pending = 205
    # status queue update by data prep worker
    Training_DataPrep_InProgress = 206

    Training_DataPrep_Success = 207
    Training_DataPrep_Failure = 208

    # Data Prep
    ###############################################
    # Kaldi

    # task in kaldi queue, but not processed by kaldi worker
    Training_Pending = 210
    # status queue update by kaldi worker (start processing)
    Training_In_Progress = 220

    Training_Success = 300
    Training_Failure = 320

    # Kaldi
    ###############################################

    @staticmethod
    def status_to_string(status):
        return {
            100: "Init",

            150: "TextPrep_Pending",
            151: "TextPrep_Failure",

            200: "Trainable",
            205: "Training_DataPrep_Pending",
            206: "Training_DataPrep_InProgress",
            207: "Training_DataPrep_Success",
            208: "Training_DataPrep_Failure",
            210: "Training_Pending",
            220: "Training_In_Progress",

            300: "Training_Success",
            320: "Training_Failure",
        }[status]


class Training(db.Model):
    __tablename__ = 'trainings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    project = db.relationship('Project')
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    version = db.Column(db.Integer, autoincrement=True)

    creation_timestamp = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow)
    status = db.Column(db.Enum(TrainingStateEnum), default=TrainingStateEnum.Init)

    prepare_callback = db.Column(db.Text, default='{}')
    train_callback = db.Column(db.Text, default='{}')

    def can_assign_resource(self):
        return self.status in (TrainingStateEnum.Init,
                               TrainingStateEnum.TextPrep_Pending,
                               TrainingStateEnum.TextPrep_Failure,
                               TrainingStateEnum.Trainable)

    def __repr__(self):
        return json.dumps(self, cls=AlchemyEncoder)
