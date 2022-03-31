import sys
from flask_signon.about import __author__, __py_versions__, __url__, __version__, __description__
from flask_signon.core.exceptions import PyVersionInvalid

if f"{sys.version_info.major}.{sys.version_info.minor}" not in __py_versions__:
    raise PyVersionInvalid()

from flask_signon.core.jwt_signon import JWTAuth
from flask_signon.core.session_signon import SessionAuth
from flask_signon.core.user import BaseUser, AnonymousUser
from flask_signon.core import exceptions
from flask_signon.views import SignOnView
from flask_signon.authenticators import JWTAuthenticator, SessionAuthenticator
from flask_signon import permissions
from flask_signon.utils import *

__all__ = (
    "JWTAuth",
    "SessionAuth",
    "BaseUser",
    "AnonymousUser",
    "exceptions",
    "loging_session",
    "logout_session",
    "current_user",
    "get_current_user",
    "SignOnView",
    "JWTAuthenticator",
    "SessionAuthenticator",
    "permissions"
)