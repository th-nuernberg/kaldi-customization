import connexion
import six
import redis
import json
import config

from openapi_server.models.project import Project  # noqa: E501
from openapi_server.models.training_status import TrainingStatus  # noqa: E501
from openapi_server import util


def create_project(body):  # noqa: E501
    """Create a new project

     # noqa: E501

    :param body: Project object that needs to be created
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Project.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


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
    :type project_uuid: str

    :rtype: Project
    """
    return 'do some magic!'


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


def update_project(body):  # noqa: E501
    """Update an existing project

     # noqa: E501

    :param body: Project object that needs to be updated
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Project.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
