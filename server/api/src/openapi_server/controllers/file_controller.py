import connexion
import six

from openapi_server.models.resource import Resource  # noqa: E501
from openapi_server import util


def create_file(body):  # noqa: E501
    """Create/Upload a new file

     # noqa: E501

    :param body: File object that needs to be created
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Resource.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_file_by_uuid(file_uuid):  # noqa: E501
    """Find file by UUID

    Returns a single file # noqa: E501

    :param file_uuid: UUID of file to return
    :type file_uuid: str

    :rtype: Resource
    """
    return 'do some magic!'
