import connexion
import six
import json

from models import db
from models.project import Project as DB_Project
from models.user import User as DB_User
from models.acousticmodel import AcousticModel as DB_AcousticModel
from models.resource import Resource as DB_Resource, ResourceStateEnum as DB_ResourceStateEnum
from models.training import Training as DB_Training, TrainingStateEnum as DB_TrainingStateEnum
from models.training_resource import TrainingResource as DB_TrainingResource

from redis_communication import create_dataprep_job, create_kaldi_job
from minio_communication import upload_to_bucket, download_from_bucket, minio_buckets, copy_object_in_bucket
from config import minio_client

from openapi_server.models.callback_object import CallbackObject  # noqa: E501
from openapi_server.models.resource import Resource  # noqa: E501
from openapi_server.models.resource_reference_object import ResourceReferenceObject  # noqa: E501
from openapi_server.models.training import Training  # noqa: E501
from openapi_server.models.data_prep_stats import DataPrepStats  # noqa: E501
from openapi_server import util


def get_decode_session_log(project_uuid, training_version, session_uuid):  # noqa: E501
    """Get decode session

    Returns the log of a decoding session # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param session_uuid: UUID of the session
    :type session_uuid: 

    :rtype: str
    """
    return 'do some magic!'


def get_perparation_log(project_uuid, training_version):  # noqa: E501
    """Get Preparation Log

    Returns the log of a preparation # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: str
    """
    return 'do some magic!'


def get_resource_log(resource_uuid):  # noqa: E501
    """Find resource by UUID

    Returns the log of a resource # noqa: E501

    :param resource_uuid: UUID of resource to return
    :type resource_uuid: str

    :rtype: str
    """
    return 'do some magic!'


def get_training_log(project_uuid, training_version):  # noqa: E501
    """Get Training Log

    Returns the log of a training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: str
    """
    return 'do some magic!'


def get_training_stats(project_uuid, training_version):  # noqa: E501
    """Get Training Stats

    Returns the stats to be reviewed before training # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: DataPrepStats
    """
    current_user = connexion.context['token_info']['user']

    db_project = DB_Project.query.filter_by(
        uuid=project_uuid, owner_id=current_user.id).first()

    if db_project is None:
        return ("Project not found", 404)

    db_training = DB_Training.query.filter_by(version=training_version) \
        .filter_by(project_id=db_project.id).first()

    if db_training is None:
        return ("Training not found", 404)

    status, stream = download_from_bucket(
        minio_client, minio_buckets["TRAINING_BUCKET"], "{}/stats.json".format(db_training.id))

    json_object = json.loads(stream.read().decode('utf-8'))
    print(json_object)
    return (DataPrepStats(unique_words_count=json_object["unique_words"],
        total_words_count=json_object["total_words_count"],
        lines_count=json_object["lines_count"],
        files_count=json_object["files_count"],
        ),200)
