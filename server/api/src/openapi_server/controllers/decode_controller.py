import connexion
import six

from openapi_server.models.decode_message import DecodeMessage  # noqa: E501
from openapi_server.models.inline_response202 import InlineResponse202  # noqa: E501
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


def start_decode(project_uuid, training_version, audio_file):  # noqa: E501
    """Decode audio to text

    Decode audio data to text using the trained project # noqa: E501

    :param project_uuid: UUID of the project
    :type project_uuid: 
    :param training_version: Training version of the project
    :type training_version: int
    :param audio_file: Audio file for decoding
    :type audio_file: str

    :rtype: InlineResponse202
    """
    return 'do some magic!'
