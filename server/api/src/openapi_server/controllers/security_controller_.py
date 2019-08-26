from typing import List
from models import OAuth2Token, User

import time


def info_from_oauth(token):
    """
    Validate and decode token.
    Returned value will be passed in 'token_info' parameter of your operation function, if there is one.
    'sub' or 'uid' will be set in 'user' parameter of your operation function, if there is one.
    'scope' or 'scopes' will be passed to scope validation function.

    :param token Token provided by Authorization header
    :type token: str
    :return: Decoded token information or None if token is invalid
    :rtype: dict | None
    """

    token = OAuth2Token.query.filter_by(access_token=token).first()

    if not token or token.is_refresh_token_expired():
        return None

    return { 'scopes': token.scope.split(), 'user': User.query.filter_by(id=token.user_id).first() }


def validate_scope_oauth(required_scopes, token_scopes):
    """
    Validate required scopes are included in token scope

    :param required_scopes Required scope to access called API
    :type required_scopes: List[str]
    :param token_scopes Scope present in token
    :type token_scopes: List[str]
    :return: True if access to called API is allowed
    :rtype: bool
    """
    return set(required_scopes).issubset(set(token_scopes))
