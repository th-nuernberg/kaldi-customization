import connexion
import six

from openapi_server.models.user import User  # noqa: E501
from openapi_server import util

from models import db
from models.user import User as DB_User
from models.auth import OAuth2Client as DB_OAuth2Client, OAuth2Token as DB_OAuth2Token

from passlib.hash import sha256_crypt
from sqlalchemy import exc
from werkzeug.security import gen_salt


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
                      email=user.email,
                      password=sha256_crypt.encrypt(user.password))

    db.session.add(db_user)

    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print("Failed to insert user into database: ", e)
        return ("Cannot create user", 400)

    db_client = DB_OAuth2Client(
        client_name='default',
        client_uri='/',
        # TODO: get all scopes from openapi.yaml
        scope='decode:projects read:projects train:projects write:projects read:resources read:audio write:resources read:user write:user write:audio',
        redirect_uri='/',
        grant_type='password',
        response_type='code',
        token_endpoint_auth_method='client_secret_basic')
    db_client.user_id = db_user.id
    db_client.client_id = gen_salt(24)
    db_client.client_secret = gen_salt(48)

    db.session.add(db_client)
    db.session.commit()

    return (User(username=db_user.username, email=db_user.email), 201)


def get_user():  # noqa: E501
    """Get current user

    Provides info about the logged in user. # noqa: E501


    :rtype: User
    """
    current_user = connexion.context['token_info']['user']

    if not current_user:
        return ("User not authorized", 403)

    return User(username=current_user.username, email=current_user.email)


def login_user(email, password):  # noqa: E501
    """Logs user into the system

     # noqa: E501

    :param email: The user name for login
    :type email: str
    :param password: The password for login in clear text
    :type password: str

    :rtype: str
    """    
    db_user = DB_User.query.filter_by(email=email).first()

    if not db_user:
        return ("Invalid email/password", 400)

    if not db_user.check_password(password):
        return ("Invalid email/password", 400)

    db_client = DB_OAuth2Client.query.filter_by(
        user_id=db_user.id,
        client_name='default').first()

    if not db_client:
        return ("Missing client for web login ('default')")

    db_token = DB_OAuth2Token(
        client_id=db_client.client_id,
        token_type='Baerer',
        access_token=gen_salt(42),
        refresh_token=None,
        scope=db_client.scope,
        revoked=0,
        expires_in=864000,
        user_id=db_user.id)

    db.session.add(db_token)
    db.session.commit()

    return db_token.access_token


def logout_user(token):  # noqa: E501
    """Logs out current logged in user session

     # noqa: E501

    :param token: Access token to revoke
    :type token: 

    :rtype: None
    """
    db_token = DB_OAuth2Token.query.filter_by(
        access_token=token).first()

    if db_token:
        db_token.revoked = 1
        db.session.add(db_token)
        db.session.commit()

    return 'do some magic!'
