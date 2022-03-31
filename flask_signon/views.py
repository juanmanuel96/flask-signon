import typing as t
from flask.views import MethodView

from flask_signon.authenticators import BaseAuthenticator
from flask_signon.core.exceptions import InvalidBaseClass
from flask_signon.permissions import BasePermission


class SignOnView(MethodView):
    authentication_classes = []
    permission_classes = []
    
    def dispatch_request(self, *args: t.Any, **kwargs: t.Any):
        for authenticator in self.authentication_classes:
            if not issubclass(authenticator, BaseAuthenticator):
                raise InvalidBaseClass('Authentication classes must '
                                       'be bassed off BaseAuthenticator')
            auth = authenticator()
            sucess, data = auth()
            if not sucess:
                return data
        
        for permission in self.permission_classes:
            if not issubclass(permission, BasePermission):
                raise InvalidBaseClass('Permission classes must '
                                       'be bassed off BasePermission')
            perm = permission(self)
            perm()
        return super().dispatch_request(*args, **kwargs)
