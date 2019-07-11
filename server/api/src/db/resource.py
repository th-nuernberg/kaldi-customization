from bootstrap import db

class Resource(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    #project = db.relationship('Project')#, backref=db.backref('project', remote_side=[id], lazy=True, cascade='all,delete'))
    project = db.Column(db.Integer,db.ForeignKey("projects.id"))
    #origin = db.relationship('File')
    origin = db.Column(db.Integer,db.ForeignKey("files.id"))

    def __repr__(self):
        return "Resource"
