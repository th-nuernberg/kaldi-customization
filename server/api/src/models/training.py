from ._db import db
import enum

class TrainingStateEnum(enum.IntEnum):
    Init = 100

    Trainable = 200
    Training_Pending = 210
    Training_In_Progress = 220
    
    Training_Success = 300
    Training_Failure = 320

    @staticmethod
    def status_to_string(status):
        return {
            100: "Init",

            200: "Trainable",
            210: "Training_Pending",
            220: "Training_In_Progress",

            300: "Training_Success",
            320: "Training_Failure"
        }[status]

class Training(db.Model):
    __tablename__ = 'trainings'

    id = db.Column(db.Integer, primary_key=True)
    
    project = db.relationship('Project')
    project_id = db.Column(db.Integer,db.ForeignKey("projects.id"))

    version = db.Column(db.Integer)
    
    create_date = db.Column(db.DateTime(timezone=False))
    status = db.Column(db.Enum(TrainingStateEnum))

    def __repr__(self):
        return self.__dict__
