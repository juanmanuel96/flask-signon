import importlib
from flask import Flask
from flask_login import LoginManager
from flask_login.utils import _user_context_processor

from flask_signon.utils import import_string


class SessionAuth(LoginManager):
    def init_app(self, app, add_context_processor=True):
        app.login_manager = self
        app.after_request(self._update_remember_cookie)

        if add_context_processor:
            app.context_processor(_user_context_processor)
        
        self._set_default_configuration_options(app)
        self.login_view = app.config.get('LOGIN_VIEW')
        self.blueprint_login_views = app.config.get('BLUEPRINT_LOGIN_VIEWS')
        self.anonymous_user = import_string(app.config.get('ANONYMOUS_USER'))

    @staticmethod
    def _set_default_configuration_options(app: Flask):
        app.config.setdefault("LOGIN_DISABLED", False)
        app.config.setdefault("LOGIN_VIEW", "login")
        app.config.setdefault("BLUEPRINT_LOGIN_VIEWS", {})
        app.config.setdefault('ANONYMOUS_USER', 'flask_signon.mixins.AnonymousUser')
