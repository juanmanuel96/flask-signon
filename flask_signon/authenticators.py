import typing as t

from flask import request, current_app
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import UserClaimsVerificationError

from flask_signon.utils import current_user
from flask_signon.core.exceptions import TokenError

EXEMPT_METHODS = set(['OPTIONS'])


class BaseAuthenticator:    
    def authenticate(self):
        """This method is called by __call__ method. It must return 

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("Override this method in your class")
    
    def __call__(self):
        return self.authenticate()


class JWTAuthenticator(BaseAuthenticator):
    def authenticate(self) -> t.Tuple[bool, t.Any]:
        """Verify that the token is not blacklisted and return the user infomration
        found in the JWT.

        Returns:
            user_data (t.Dict): User information found in the JWT
        """
        if request.method in EXEMPT_METHODS:
            return True, None
        elif current_app.config.get('LOGIN_DISABLED'):
            return True, None
        else:
            try:
                verify_jwt_in_request()
            except UserClaimsVerificationError:
                # Custom exception
                raise TokenError('Token is blacklisted')
            return True, None


class SessionAuthenticator(BaseAuthenticator):
    def authenticate(self):
        if request.method in EXEMPT_METHODS:
            return True, None  # Do not authenticate, not required
        elif current_app.config.get('LOGIN_DISABLED'):
            return True, None  # Do not authenticate, not required
        elif not current_user.is_authenticated:
            # If not authenticated, throw user to login page
            return False, current_app.login_manager.unauthorized()
        else:
            return True, None
