# -*- coding: utf-8 -*-

from django.utils.crypto import salted_hmac

from django_restful import RestfulApiError

from django_sae.models.user import UserModel


class UserWrapper(object):

    def __init__(self, user):
        if not isinstance(user, dict):
            user = user.__dict__

        for k, v in user.iteritems():
            setattr(self, k.lower(), v)

        self.pk = self.id
        self.password = self.login_password
        self.is_authenticated = self.authenticated

    def save(self, **field):
        pass

    def authenticated(self):
        return True

    def get_session_auth_hash(self):
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()

    def get_username(self):
        """ 获取用户姓名，用于djangorestframework-jwt获取api-token-auth接口时需要。
        """
        try:
            username = self.user_name
        except AttributeError:
            username = '{}{}'.format(self.first_name, self.last_name)
        return username


class ModelBackend(object):
    """
    Authenticates against django.contrib.auth.models.User.
    """
    supports_inactive_user = True

    # TODO: Model, login attribute name and password attribute name should be
    # configurable.
    def authenticate(self, username=None, password=None):
        try:
            _service = UserModel()
            user = _service.authenticate(username, password)
            return UserWrapper(user)
        except RestfulApiError:
            return None

    def get_user(self, user_id):
        try:
            _service = UserModel()
            user = _service.get_user(user_id)
            return UserWrapper(user)
        except RestfulApiError:
            return None

    def get_permissions(self, user_id):
        """ 根据用户id获取用户权限
        """
        try:
            _service = UserModel()
            permissions = _service.get_permissions(user_id)
            return permissions
        except RestfulApiError as ex:
            return None
