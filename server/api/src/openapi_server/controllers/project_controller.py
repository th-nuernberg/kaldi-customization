import connexion
import six
import redis
import json
import config

from openapi_server.models.acoustic_model import AcousticModel
from openapi_server.models.acoustic_model_type import AcousticModelType
from openapi_server.models.create_project_object import CreateProjectObject  # noqa: E501
from openapi_server.models.project import Project  # noqa: E501
from openapi_server.models.training_status import TrainingStatus  # noqa: E501
from openapi_server import util

from models import db, Project as DB_Project, TrainingStateEnum as DB_TrainingStateEnum, User as DB_User, AcousticModel as DB_AcousticModel

from mapper import mapper

def create_project(create_project_object=None):  # noqa: E501
    """Create a new project

     # noqa: E501

    :param create_project_object: Project object that needs to be created
    :type create_project_object: dict | bytes

    :rtype: Project
    """
    if connexion.request.is_json:
        create_project_object = CreateProjectObject.from_dict(connexion.request.get_json())  # noqa: E501
    else:
        return (405, 'Invalid input')

    # Resolve acoustic model
    db_acousticModel = DB_AcousticModel.query.filter_by(uuid=create_project_object.acoustic_model).first()

    if not db_acousticModel:
        return ("Acoustic Model not found", 404)

    my_user = DB_User.query.get(1)

    db_proj = DB_Project(
        #api_token=str(uuid.uuid4().hex) + str(uuid.uuid4().hex),
        name=create_project_object.name,
        owner=my_user,
        acoustic_model=db_acousticModel
        #TODO: how to set parent model?
    )
    db.session.add(db_proj)
    db.session.commit()

    return mapper.db_project_to_front(db_proj)


def download_training_result(project_uuid):  # noqa: E501
    """Find project training results by UUID

    Returns an archive # noqa: E501

    :param project_uuid: UUID of project training result to return
    :type project_uuid: str

    :rtype: file
    """
    return 'do some magic!'


def get_project_by_uuid(project_uuid):  # noqa: E501
    """Find project by UUID

    Returns a single project # noqa: E501

    :param project_uuid: UUID of project to return
    :type project_uuid: 

    :rtype: Project
    """

    #TODO: check the ownership of the file
    # db_file.owner

    db_proj = DB_Project.query.filter_by(uuid=project_uuid).first()

    if (db_proj is None):
        return ("Project not found", 404)

    return mapper.db_project_to_front(db_proj)

'''
def train_project(project_uuid):  # noqa: E501
    """Train current project

     # noqa: E501

    :param project_uuid: Project object that needs to be trained
    :type project_uuid: str

    :rtype: TrainingStatus
    """
    entry = {
        "acoustic-model-bucket" : config.minio_buckets.ACOUSTIC_MODELS_BUCKET,
        "acoustic-model-id" : 1,
        "project-bucket" : config.minio_buckets.LANGUAGE_MODELS_BUCKET,
        "project-uuid" : project_uuid
    }
    redis_conn.rpush("QUEUE", json.dumps(entry))
    return TrainingStatus.Training_Pending

'''
