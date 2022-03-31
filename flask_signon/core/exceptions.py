class BaseFlaskSignonException(Exception):
    default_message: str = None
    
    def __init__(self, message: str = None) -> None:
        if not message:
            message = self.default_message
        super().__init__(message)


class PyVersionInvalid(BaseFlaskSignonException):
    default_message = 'Python version is not equal or greater than 3'


class TokenError(BaseFlaskSignonException):
    default_message = "Provided access token is blacklisted"


class InvalidBaseClass(BaseFlaskSignonException):
    default_message = "Invalid base class"


class UnauthorizedAccess(BaseFlaskSignonException):
    default_message = "Unauthorized access"
