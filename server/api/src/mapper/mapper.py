from openapi_server.models.acoustic_model import AcousticModel
from openapi_server.models.acoustic_model_type import AcousticModelType
from openapi_server.models.project import Project
from openapi_server.models.training_status import TrainingStatus
from openapi_server.models.user import User
from openapi_server.models.language import Language
from openapi_server.models.resource import Resource
from openapi_server.models.resource_type import ResourceType
from openapi_server.models.resource_status import ResourceStatus

from models import db, Project as DB_Project, TrainingStateEnum as DB_TrainingStateEnum, User as DB_User, AcousticModel as DB_AcousticModel

def db_project_to_front(db_project):
    if db_project.parent:
        parent_uuid = db_project.parent.uuid
    else:
        parent_uuid = None

    return Project(
        name=db_project.name,
        uuid=db_project.uuid,
        acoustic_model=db_acousticModel_to_front(db_project.acoustic_model),
        parent=parent_uuid,
        #trainings=.,
        creation_timestamp=db_project.create_date,
        owner=db_user_to_front(db_project.owner)
    )

def db_acousticModel_to_front(db_acousticModel):
    return AcousticModel(
        uuid=db_acousticModel.uuid,
        name=db_acousticModel.name,
        language=db_language_to_front(db_acousticModel.language),
        model_type=AcousticModelTypeEnum_to_AcousticModelType(db_acousticModel.model_type)
    )

def db_user_to_front(db_user):
    return User(
        id=db_user.id,
        username=db_user.username
    )

def db_language_to_front(db_language):
    return Language(
        id=db_language.id,
        name=db_language.name
    )

def db_resource_to_front(db_resource):
    return Resource(
        name=db_resource.name, 
        status=ResourceStatus.ResourceStateEnum_to_ResourceStatus(db_resource.status),
        resource_type=ResourceTypeEnum_to_ResourceType(db_resource.resource_type),
        uuid=db_resource.uuid,
        creation_timestamp=db_resource.upload_date
    )

def ResourceTypeEnum_to_ResourceType(resourceType):
    return {
        1: ResourceType.html,
        2: ResourceType.docx,
        3: ResourceType.txt,
        4: ResourceType.pdf,
        5: ResourceType.png,
        6: ResourceType.jpg
        }[resourceType]

def ResourceStateEnum_to_ResourceStatus(resourceState):
    return {
        0: ResourceStatus.Upload_InProgress,
        1: ResourceStatus.Upload_Failure,
        9: ResourceStatus.TextPreparation_Ready,

        10: ResourceStatus.TextPreparation_Pending,
        11: ResourceStatus.TextPreparation_InProcess,
        12: ResourceStatus.TextPreparation_Failure,
        13: ResourceStatus.TextPreparation_Success
        }[resourceState]

def AcousticModelTypeEnum_to_AcousticModelType(modelType):
        return {
            100: AcousticModelType.HMM_GMM,
            200: AcousticModelType.HMM_DNN,
            300: AcousticModelType.HMM_RNN
            }[modelType]
