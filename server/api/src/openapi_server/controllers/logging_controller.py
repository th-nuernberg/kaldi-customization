import connexion
import six

from openapi_server.models.data_prep_stats import DataPrepStats  # noqa: E501
from openapi_server import util


def get_perparation_log(project_uuid, training_version):  # noqa: E501
    """Get Training Log

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
    return 'do some magic!'
