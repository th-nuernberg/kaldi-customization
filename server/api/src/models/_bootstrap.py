from ._db import db
from .language import Language
from .acousticmodel import AcousticModel, ModelType


def bootstrap():
    """Setup dummy stuff for database"""

    german = Language(name="German")
    db.session.add(german)

    acoustic_model = AcousticModel(name='Voxforge', language=german.id, model_type=ModelType.HMM_RNN)
    db.session.add(acoustic_model)
    """
    root_model = Model(project=root_project)
    db.session.add(root_model)

    project1 = Project(uuid='project#1', name='Test Project')
    db.session.add(project1)

    resource1 = Resource(model=root_model, name='res0', resource_type=FileTypeEnum.modelresult , file_type=FileTypeEnum.png, status=FileStateEnum.Upload_InProgress)
    db.session.add(resource1)
    app.logger.info(resource1)

    derived_model0 = Model(project=project1, parent=root_model)
    db.session.add(derived_model0)

    derived_model1 = Model(project=project1, parent=root_model)
    db.session.add(derived_model1)
    """
    db.session.commit()

    #app.logger.info(root_model.children)
    #app.logger.info(derived_model0.parent.project.name)

    db.session.close()
