from ._db import db
import enum

class ProjectStateEnum(enum.IntEnum):
    Init = 100

    Trainable = 200
    Train_Pending = 210
    Train_In_Progress = 220
    
    Train_Success = 300
    Train_Failure = 320

    @staticmethod
    def status_to_string(status):
        return {
            100: "Init",

            200: "Trainable",
            210: "Train_Pending",
            220: "Train_In_Progress",

            300: "Train_Success",
            320: "Train_Failure"
        }[status]


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    API_token = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(255))
    #owner = db.relationship('User')#, backref=db.backref('project', remote_side=[id], lazy=True, cascade='all,delete'))
    owner = db.Column(db.Integer,db.ForeignKey("users.id"))
    #acoustic_model = db.relationship('AcousticModel')
    acoustic_model = db.Column(db.Integer,db.ForeignKey("acousticmodels.id"))
    #parent = db.relationship('Project')
    parent = db.Column(db.Integer,db.ForeignKey("projects.id"))

    file_type = db.Column(db.Enum(ProjectStateEnum), nullable=True)


    def __repr__(self):
        return '<Project #{} (UUID: {})>'.format(self.id, self.uuid)
