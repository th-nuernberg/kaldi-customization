from openapi_server.models.acoustic_model import AcousticModel
from openapi_server.models.acoustic_model_type import AcousticModelType
from openapi_server.models.project import Project
from openapi_server.models.training import Training
from openapi_server.models.training_status import TrainingStatus
from openapi_server.models.user import User
from openapi_server.models.language import Language
from openapi_server.models.resource import Resource
from openapi_server.models.resource_type import ResourceType
from openapi_server.models.resource_status import ResourceStatus
from openapi_server.models.audio import Audio
from openapi_server.models.audio_status import AudioStatus

from models import db, Project as DB_Project, TrainingStateEnum as DB_TrainingStateEnum, User as DB_User, AcousticModel as DB_AcousticModel
from models.training_resource import TrainingResource as DB_TrainingResource
from models.training import Training as DB_Training

def db_project_to_front(db_project):
    if db_project.parent:
        parent_uuid = db_project.parent.uuid
    else:
        parent_uuid = None

    #TODO filter by user?
    trainings = DB_Training.query.filter_by(project=db_project).all()

    if trainings:
        training_list = [ db_training_to_front(t) for t in trainings ]
    else:
        training_list = []

    return Project(
        name=db_project.name,
        uuid=db_project.uuid,
        acoustic_model=db_acousticModel_to_front(db_project.acoustic_model),
        parent=parent_uuid,
        trainings=training_list,
        creation_timestamp=db_project.create_date,
        owner=db_user_to_front(db_project.owner)
    )

def db_acousticModel_to_front(db_acousticModel):
    return AcousticModel(
        uuid=db_acousticModel.uuid,
        name=db_acousticModel.name,
        language=db_language_to_front(db_acousticModel.language),
        model_type=db_acousticModel.model_type
    )

def db_user_to_front(db_user):
    return User(
        username=db_user.username,
        email=db_user.email
    )

def db_language_to_front(db_language):
    return Language(
        id=db_language.id,
        name=db_language.name
    )

def db_resource_to_front(db_resource):
    return Resource(
        name=db_resource.name,
        status=db_resource.status,
        resource_type=db_resource.resource_type,
        uuid=db_resource.uuid,
        creation_timestamp=db_resource.upload_date
    )

def db_training_to_front(db_training):
    # TODO filter by user?
    resources = DB_TrainingResource.query.filter_by(training=db_training).all()

    if resources:
        resource_list = [db_training_resource_to_front(r) for r in resources]
    else:
        resource_list = []

    return Training(
        version=db_training.version,
        creation_timestamp=db_training.create_date,
        status=db_training.status,
        resources=resource_list
    )

def db_audio_to_front(db_audio):
    return Audio(
        uuid=db_audio.uuid,
        name=db_audio.name,
        creation_timestamp=db_audio.upload_date,
        status=db_audio.status
    )

def db_training_resource_to_front(db_training_resource):
    return db_resource_to_front(db_training_resource.origin)
