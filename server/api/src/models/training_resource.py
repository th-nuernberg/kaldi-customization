from ._db import db

class TrainingResource(db.Model):
    __tablename__ = 'training_resources'

    id = db.Column(db.Integer, primary_key=True)
    
    training = db.relationship('Training')
    training_id = db.Column(db.Integer,db.ForeignKey("trainings.id"))
    
    origin = db.relationship('Resource')
    origin_id = db.Column(db.Integer,db.ForeignKey("resources.id"))

    def __repr__(self):
        return self.__dict__
