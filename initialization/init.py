import importlib
import importlib.machinery
importlib.machinery.SourceFileLoader('minio_communication','shared/minio_communication.py').load_module()
importlib.machinery.SourceFileLoader('models','server/api/src/models/__init__.py').load_module()
from models import *

import minio
import logging

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

with app.app_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    german = Language(name="German")
    db.session.add(german)

    english = Language(name="English")
    db.session.add(english)


    acoustic_model = AcousticModel(name='Voxforge-RNN', language=german, model_type=ModelType.HMM_RNN)
    db.session.add(acoustic_model)

    user = User(username = "kaldi" , pw_hash="213123123", salt = "Dino")
    db.session.add(user)

    test_project = Project(name = "TestProject", uuid = "12345678901234567890123456789012", api_token = "Hallo", owner = user,acoustic_model = acoustic_model, status = ProjectStateEnum.Init)
    db.session.add(test_project)
    
    db.session.commit()
    db.session.close()
