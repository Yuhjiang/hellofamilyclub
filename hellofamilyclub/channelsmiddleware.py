

from django.db import close_old_connections
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode


class TokenAuthMiddleware(object):
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        close_old_connections()
        headers = dict(scope['headers'])
