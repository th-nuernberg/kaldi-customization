import connexion
import six

from openapi_server.models.binary_decode_object import BinaryDecodeObject  # noqa: E501
from openapi_server.models.decode_message import DecodeMessage  # noqa: E501
from openapi_server.models.decode_task_reference import DecodeTaskReference  # noqa: E501
from openapi_server import util


def get_decode_result(project_uuid, training_version, decode_uuid):  # noqa: E501
    """Get the result of a decoding task

    Returns the result of a decoding task # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param decode_uuid: UUID of the decoding task
    :type decode_uuid: 

    :rtype: DecodeMessage
    """
    return 'do some magic!'


def get_decodings(project_uuid, training_version):  # noqa: E501
    """List of all decodings

    Returns a list of all decodings for this training version # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int

    :rtype: List[DecodeMessage]
    """
    return 'do some magic!'


def start_decode(project_uuid, training_version, binary_decode_object):  # noqa: E501
    """Decode audio to text

    Decode audio data to text using the trained project # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param binary_decode_object: 
    :type binary_decode_object: dict | bytes

    :rtype: DecodeTaskReference
    """
    if connexion.request.is_json:
        binary_decode_object = BinaryDecodeObject.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
