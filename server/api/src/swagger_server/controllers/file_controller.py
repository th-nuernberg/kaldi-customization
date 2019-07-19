import connexion
import six

java.io.File  # noqa: E501
from swagger_server import util


def create_file(body):  # noqa: E501
    """Create/Upload a new file

     # noqa: E501

    :param body: File object that needs to be created
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = File.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_file_by_uuid(fileUuid):  # noqa: E501
    """Find file by UUID

    Returns a single file # noqa: E501

    :param fileUuid: UUID of file to return
    :type fileUuid: str

    :rtype: File
    """
    return 'do some magic!'
