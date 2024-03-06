from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
# from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError


@database_sync_to_async
def get_user_from_token(token):
    try:
        # Delayed import to avoid issues during app startup
        from rest_framework_simplejwt.state import token_backend
        from django.contrib.auth.models import AnonymousUser

        validated_token = token_backend.decode(token)
        user_id = validated_token.get('user_id')

        print("validated_token", validated_token)
        print("user_id", user_id)

        # Delayed import to prevent importing models at top-level
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.get(id=user_id)
    except (ValidationError, User.DoesNotExist):
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    """
    Custom token authentication middleware for Django Channels.
    """

    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser

        query_string = parse_qs(scope.get('query_string', '').decode('utf-8'))
        token = query_string.get('token', [None])[0]

        print("query_string", query_string)
        print("token", token)

        if token:
            scope['user'] = await get_user_from_token(token)
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
