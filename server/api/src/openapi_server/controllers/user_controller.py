import connexion
import six

from openapi_server.models.user import User  # noqa: E501
from openapi_server import util

from models import db
from models.user import User as DB_User

from sqlalchemy import exc
from passlib.hash import sha256_crypt


def create_user(user=None):  # noqa: E501
    """Create user

    This can only be done by the logged in user. # noqa: E501

    :param user: Created user object
    :type user: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        user = User.from_dict(connexion.request.get_json())  # noqa: E501

    # TODO: implement more intelligent checks for valid email addresses
    #       and secure passwords
    if not user.username or not user.password or not user.email:
        return ("Invalid username/password/email", 400)

    db_user = DB_User(username=user.username,
                      user_email=user.email,
                      pw_hash=sha256_crypt.encrypt(user.password))

    db.session.add(db_user)

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print("Failed to insert user into database: ", e)
        return ("Cannot create user", 400)

    return (User(username=db_user.username, email=db_user.user_email),201)


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
