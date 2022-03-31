import datetime
from flask import Flask
from flask_jwt_extended import JWTManager

from flask_signon.utils import import_string


class JWTAuth(JWTManager):
    def init_app(self, app):
        """
        Register this extension with the flask app.

        :param app:
            The Flask Application object
        """
        # Save this so we can use it later in the extension
        if not hasattr(app, "extensions"):  # pragma: no cover
            app.extensions = {}
        app.extensions["flask-jwt-extended"] = self
        app.jwt_auth = self

        # Set all the default configurations for this extension
        self._set_default_configuration_options(app)
        self._set_error_handler_callbacks(app)
        self.anonymous_user = import_string(app.config.get('ANONYMOUS_USER'))
    
    @staticmethod
    def _set_default_configuration_options(app: Flask):
        # Flask-JWT-Extended configurations
        app.config.setdefault(
            "JWT_ACCESS_TOKEN_EXPIRES", datetime.timedelta(minutes=15)
        )
        app.config.setdefault("JWT_ACCESS_COOKIE_NAME", "access_token_cookie")
        app.config.setdefault("JWT_ACCESS_COOKIE_PATH", "/")
        app.config.setdefault("JWT_ACCESS_CSRF_COOKIE_NAME", "csrf_access_token")
        app.config.setdefault("JWT_ACCESS_CSRF_COOKIE_PATH", "/")
        app.config.setdefault("JWT_ACCESS_CSRF_FIELD_NAME", "csrf_token")
        app.config.setdefault("JWT_ACCESS_CSRF_HEADER_NAME", "X-CSRF-TOKEN")
        app.config.setdefault("JWT_ALGORITHM", "HS256")
        app.config.setdefault("JWT_COOKIE_CSRF_PROTECT", True)
        app.config.setdefault("JWT_COOKIE_DOMAIN", None)
        app.config.setdefault("JWT_COOKIE_SAMESITE", None)
        app.config.setdefault("JWT_COOKIE_SECURE", False)
        app.config.setdefault("JWT_CSRF_CHECK_FORM", False)
        app.config.setdefault("JWT_CSRF_IN_COOKIES", True)
        app.config.setdefault("JWT_CSRF_METHODS", ["POST", "PUT", "PATCH", "DELETE"])
        app.config.setdefault("JWT_DECODE_ALGORITHMS", None)
        app.config.setdefault("JWT_DECODE_AUDIENCE", None)
        app.config.setdefault("JWT_DECODE_ISSUER", None)
        app.config.setdefault("JWT_DECODE_LEEWAY", 0)
        app.config.setdefault("JWT_ENCODE_AUDIENCE", None)
        app.config.setdefault("JWT_ENCODE_ISSUER", None)
        app.config.setdefault("JWT_ERROR_MESSAGE_KEY", "msg")
        app.config.setdefault("JWT_HEADER_NAME", "Authorization")
        app.config.setdefault("JWT_HEADER_TYPE", "Bearer")
        app.config.setdefault("JWT_IDENTITY_CLAIM", "sub")
        app.config.setdefault("JWT_JSON_KEY", "access_token")
        app.config.setdefault("JWT_PRIVATE_KEY", None)
        app.config.setdefault("JWT_PUBLIC_KEY", None)
        app.config.setdefault("JWT_QUERY_STRING_NAME", "jwt")
        app.config.setdefault("JWT_QUERY_STRING_VALUE_PREFIX", "")
        app.config.setdefault("JWT_REFRESH_COOKIE_NAME", "refresh_token_cookie")
        app.config.setdefault("JWT_REFRESH_COOKIE_PATH", "/")
        app.config.setdefault("JWT_REFRESH_CSRF_COOKIE_NAME", "csrf_refresh_token")
        app.config.setdefault("JWT_REFRESH_CSRF_COOKIE_PATH", "/")
        app.config.setdefault("JWT_REFRESH_CSRF_FIELD_NAME", "csrf_token")
        app.config.setdefault("JWT_REFRESH_CSRF_HEADER_NAME", "X-CSRF-TOKEN")
        app.config.setdefault("JWT_REFRESH_JSON_KEY", "refresh_token")
        app.config.setdefault("JWT_REFRESH_TOKEN_EXPIRES", datetime.timedelta(days=30))
        app.config.setdefault("JWT_SECRET_KEY", None)
        app.config.setdefault("JWT_SESSION_COOKIE", True)
        app.config.setdefault("JWT_TOKEN_LOCATION", ("headers",))
        app.config.setdefault("JWT_ENCODE_NBF", True)
        
        # Flask-SignOn configurations
        app.config.setdefault('ANONYMOUS_USER', 'flask_signon.core.user.AnonymousUser')
