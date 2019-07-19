import connexion
import six

from openapi_server.models.training_status import TrainingStatus  # noqa: E501
from openapi_server import util


def download_training_result(project_uuid):  # noqa: E501
    """Find project training results by UUID

    Returns an archive # noqa: E501

    :param project_uuid: UUID of project training result to return
    :type project_uuid: str

    :rtype: file
    """
    return 'do some magic!'


def train_project(project_uuid):  # noqa: E501
    """Train current project

     # noqa: E501

    :param project_uuid: Project object that needs to be trained
    :type project_uuid: str

    :rtype: TrainingStatus
    """
    return 'do some magic!'
