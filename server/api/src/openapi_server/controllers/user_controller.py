import connexion
import six

from openapi_server.models.user import User  # noqa: E501
from openapi_server import util


def create_user(user):  # noqa: E501
    """Create user

    This can only be done by the logged in user. # noqa: E501

    :param user: Created user object
    :type user: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_user():  # noqa: E501
    """Get current user

    Provides info about the logged in user. # noqa: E501


    :rtype: User
    """
    return 'do some magic!'


def login_user(email, password):  # noqa: E501
    """Logs user into the system

     # noqa: E501

    :param email: The user name for login
    :type email: str
    :param password: The password for login in clear text
    :type password: str

    :rtype: None
    """
    return 'do some magic!'


def logout_user():  # noqa: E501
    """Logs out current logged in user session

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'
