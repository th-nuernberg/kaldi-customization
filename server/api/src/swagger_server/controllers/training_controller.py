import connexion
import six

from swagger_server.models.binary import Binary  # noqa: E501
from swagger_server.models.training_status import TrainingStatus  # noqa: E501
from swagger_server import util


def download_training_result(projectUuid):  # noqa: E501
    """Find project training results by UUID

    Returns an archive # noqa: E501

    :param projectUuid: UUID of project training result to return
    :type projectUuid: str

    :rtype: Binary
    """
    return 'do some magic!'


def train_project(projectUuid):  # noqa: E501
    """Train current project

     # noqa: E501

    :param projectUuid: Project object that needs to be trained
    :type projectUuid: str

    :rtype: TrainingStatus
    """
    return 'do some magic!'
