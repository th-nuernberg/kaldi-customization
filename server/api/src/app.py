#!/usr/local/bin/python3
from bootstrap import *


root_project = Project(uuid='root', name='Test Project')
db.session.add(root_project)
root_model = Model(project=root_project)
db.session.add(root_model)

project1 = Project(uuid='project#1', name='Test Project')
db.session.add(project1)

resource1 = Resource(model=root_model, file_name='res0', file_type=ResourceTypeEnum.PNG, status=ResourceStateEnum.Upload_InProgress)
db.session.add(resource1)
print(resource1)

derived_model0 = Model(project=project1, parent=root_model)
db.session.add(derived_model0)

derived_model1 = Model(project=project1, parent=root_model)
db.session.add(derived_model1)

db.session.commit()

print(root_model.children)
print(derived_model0.parent.project.name)

@app.route('/')
def hello():
    return 'Hello World!'
