import importlib
import importlib.machinery
importlib.machinery.SourceFileLoader('minio_communication','shared/minio_communication.py').load_module()
importlib.machinery.SourceFileLoader('models','server/api/src/models/__init__.py').load_module()
from models import *

import minio

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

REDIS_PASSWORD="kalditproject"

MINIO_ACCESS_KEY="AKIAIOSFODNN7EXAMPLE"
MINIO_SECRET_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

MYSQL_ROOT_PASSWORD="kalditproject"
MYSQL_USER="api"
MYSQL_PASSWORD="api-server-password"
MYSQL_DATABASE="api"


minio_client = minio.Minio("localhost:9001",access_key=MINIO_ACCESS_KEY,secret_key=MINIO_SECRET_KEY,secure=False)

app = Flask('__APP')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}:{}/{}'.format(MYSQL_USER, MYSQL_PASSWORD, "127.0.0.1", 3307, MYSQL_DATABASE)

#db = SQLAlchemy(app= app)
with app.app_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()
    #db.init_app(app)
    #db.session.commit()

    exit()
    #Setup dummy stuff for database
    german = Language(name="German")
    db.session.add(german)




    acoustic_model = AcousticModel(name='Voxforge-RNN', language=german.id, model_type=ModelType.HMM_RNN)
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
