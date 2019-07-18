import connexion
import six

from swagger_server.models.project import Project  # noqa: E501
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


def delete_project(project_uuid, api_key=None):  # noqa: E501
    """Deletes a project

     # noqa: E501

    :param project_uuid: Project UUID to delete
    :type project_uuid: str
    :param api_key: 
    :type api_key: str

    :rtype: None
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
