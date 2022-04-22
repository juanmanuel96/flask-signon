from flask import current_app, request

from flask_signon.core.exceptions import UnauthorizedAccess
from flask_signon.utils import current_user



__all__ = (
    "BasePermission",
    "IsAuthenticated",
    "IsStaff",
    "IsSuperuser",
    "IsActive"
)


class BasePermission:
    def __init__(self, view) -> None:
        """Base class for Permission classes.
        
        The check_permision method must be overriden with the desried permission 
        verification and return a boolean value.
        """
        try:
            self.view = view.__name__
        except AttributeError:
            try:
                self.view = view.name
            except AttributeError:
                self.view = request.endpoint
        self.permission_purpose = None

    def check_permission(self) -> bool:
        raise NotImplementedError('Override this method with custom permission '\
                                  'check')
    
    def __call__(self):
        """Will call the check_permission method. If the method returns false then 
        an unauthorized exception will be raised.
        """
        if not current_app.config.get('PERMISSION_CHECK',  True):
            return
        if not self.check_permission():
            msg = f"User does not have permission to view {self.view}"
            if self.permission_purpose:
                msg = msg + f' because they are not {self.permission_purpose}'
            raise UnauthorizedAccess(msg)


class IsActive(BasePermission):
    def check_permission(self) -> bool:
        return current_user.is_active


class IsAuthenticated(IsActive):
    def __init__(self, view) -> None:
        super().__init__(view)
        self.permission_purpose = 'authenticated'
    
    def check_permission(self):
        return super().check_permission() and current_user.is_authenticated


class IsStaff(IsActive):
    def __init__(self, view) -> None:
        super().__init__(view)
        self.permission_purpose = 'staff member'
    
    def check_permission(self):
        return super().check_permission() and current_user.is_staff 


class IsSuperuser(IsActive):
    def __init__(self, view) -> None:
        super().__init__(view)
        self.permission_purpose = 'admin'
    
    def check_permission(self):
        return super().check_permission() and current_user.is_superuser
