import connexion
import six

from swagger_server.models.binary import Binary  # noqa: E501
from swagger_server.models.project import Project  # noqa: E501
from swagger_server.models.training_status import TrainingStatus  # noqa: E501
from swagger_server import util


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


def download_training_result(projectUuid):  # noqa: E501
    """Find project training results by UUID

    Returns an archive # noqa: E501

    :param projectUuid: UUID of project training result to return
    :type projectUuid: str

    :rtype: Binary
    """
    return 'do some magic!'


def get_project_by_uuid(projectUuid):  # noqa: E501
    """Find project by UUID

    Returns a single project # noqa: E501

    :param projectUuid: UUID of project to return
    :type projectUuid: str

    :rtype: Project
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
