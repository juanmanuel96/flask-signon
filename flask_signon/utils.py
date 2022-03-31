import importlib
from werkzeug.local import LocalProxy
from flask import _request_ctx_stack, has_request_context, session, current_app, request
from flask_jwt_extended import get_jwt
from flask_login.signals import user_logged_in, user_logged_out
from flask_signon.core.user import BaseUser


__all__ = (
    'current_user',
    'get_current_user',
    'signin_user',
    'logout_session'
)


COOKIE_NAME = 'remember_token'


class NotJWTAuth(Exception):
    pass

class UserNotSignedOn(Exception):
    pass

class NotValidUserType(Exception):
    pass


current_user = LocalProxy(lambda: get_current_user())


def get_current_user():
    anon_user = import_string(current_app.config['ANONYMOUS_USER'])
    try:
        return jwt_auth()
    except NotJWTAuth:
        # Do nothing, try with session login
        pass
    try:
        return _get_user()
    except UserNotSignedOn:
        # Do nothing, must be anon user
        pass
    return anon_user()  # Will get here only if previous attempts were not successfull


def jwt_auth():
    try:
        get_jwt() # Raises error if no JWT is present and view is not optional
    except RuntimeError:
        raise NotJWTAuth()
    
    jwt_user_dict = getattr(_request_ctx_stack.top, "jwt_user", None)
    if jwt_user_dict is None:
        raise RuntimeError(
            "You must provide a `@app.jwt.user_lookup_loader` callback to use "
            "this method"
        )
    loaded_user = jwt_user_dict["loaded_user"]
    if not issubclass(type(loaded_user), BaseUser):
        raise NotValidUserType("User type must be a subclass of :class:`BaseUser`")
    return loaded_user


def _get_user():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        current_app.login_manager._load_user()
    user = getattr(_request_ctx_stack.top, 'user', None)
    if user is None:  
        # Should never get here since session auth will either be a developer defined
        # User or AnonymousUser
        raise UserNotSignedOn()
    if not issubclass(type(user), BaseUser):
        raise NotValidUserType("User type must be a subclass of :class:`BaseUser`")

    return user


def signin_user(user, remember=False, duration=None, force=False, fresh=True):
    '''
    ## OVERRIDES FLASK-LOGIN LOGIN_USER FUNCTION TO MEET FLASK-SIGNON STANDARD.
    '''
    if not force and not user.is_active:
        return False

    user_id = getattr(user, current_app.login_manager.id_attribute)()
    session['_user_id'] = user_id
    session['_fresh'] = fresh
    session['_id'] = current_app.login_manager._session_identifier_generator()

    if remember:
        session['_remember'] = 'set'
        if duration is not None:
            try:
                # equal to timedelta.total_seconds() but works with Python 2.6
                session['_remember_seconds'] = (duration.microseconds +
                                                (duration.seconds +
                                                 duration.days * 24 * 3600) *
                                                10**6) / 10.0**6
            except AttributeError:
                raise Exception('duration must be a datetime.timedelta, '
                                'instead got: {0}'.format(duration))

    current_app.login_manager._update_request_context_with_user(user)
    user_logged_in.send(current_app._get_current_object(), user=_get_user())
    return True


def logout_session():
    user = _get_user()

    if '_user_id' in session:
        session.pop('_user_id')

    if '_fresh' in session:
        session.pop('_fresh')

    if '_id' in session:
        session.pop('_id')

    cookie_name = current_app.config.get('REMEMBER_COOKIE_NAME', COOKIE_NAME)
    if cookie_name in request.cookies:
        session['_remember'] = 'clear'
        if '_remember_seconds' in session:
            session.pop('_remember_seconds')

    user_logged_out.send(current_app._get_current_object(), user=user)
    current_app.login_manager._update_request_context_with_user()
    return True


def import_string(dot_path):
    path_split = dot_path.split('.')
    desired = path_split.pop(-1)
    module = importlib.import_module('.'.join(path_split))
    return getattr(module, desired)
