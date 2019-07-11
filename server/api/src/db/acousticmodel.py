from bootstrap import db
import enum

class ModelType(enum.IntEnum):
    HMM_GMM = 100
    HMM_DNN = 200
    HMM_RNN = 300


    def type_to_string(status):
        return {
            100: "HMM_GMM",
            200: "HMM_DNN",
            300: "HMM_RNN"
            }[status]

class AcousticModel(db.Model):
    __tablename__ = 'acousticmodels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    #language = db.relationship('Language')#, backref=db.backref('project', remote_side=[id], lazy=True, cascade='all,delete'))
    language = db.Column(db.Integer,db.ForeignKey("languages.id"))
    model_type = db.Column(db.Enum(ModelType), nullable=True)

    def __repr__(self):
        return '{{"id":{},"name":{},"language":{},"model_type":{}}}'.format(self.id, self.name,self.language.name,ModelType.type_to_string(self.model_type))