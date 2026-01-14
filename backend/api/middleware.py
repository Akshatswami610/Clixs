from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication

@database_sync_to_async
def get_user_from_token(token):
    jwt_auth = JWTAuthentication()
    validated_token = jwt_auth.get_validated_token(token)
    return jwt_auth.get_user(validated_token)


class JwtAuthMiddleware:
    """
    Custom JWT auth middleware for Django Channels.
    Expects ?token=<JWT> in query string.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        scope["user"] = AnonymousUser()

        query_string = scope.get("query_string", b"").decode()
        if "token=" in query_string:
            token = query_string.split("token=")[-1]
            try:
                scope["user"] = await get_user_from_token(token)
            except Exception:
                scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)
