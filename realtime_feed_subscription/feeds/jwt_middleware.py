from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from channels.auth import AuthMiddlewareStack
from .models import User
from channels.db import database_sync_to_async


class JWTAuthMiddleware:
    """
    JWT Authentication Middleware.

    This class implements a middleware for JWT authentication.
    It extracts the JWT token from the request headers, decodes it,
    and retrieves the associated user from the database.
    The user is then added to the request scope for further processing.

    Args:
        inner: The inner middleware or application.

    Returns:
        The response from the inner middleware or application.

    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        auth_header = headers.get(b"authorization")
        if auth_header:
            try:
                auth_token = auth_header.decode().split()[1]
                decoded_token = AccessToken(auth_token)
                user_id = decoded_token.payload.get("user_id")
                user = await database_sync_to_async(User.objects.get)(id=user_id)
                scope["user"] = user
            except IndexError:
                scope["user"] = AnonymousUser()
                scope["error"] = "Please Provide Proper Valid Bearer Token"
            except Exception as e:
                scope["user"] = AnonymousUser()
                scope["error"] = str(e)
        else:
            scope["user"] = AnonymousUser()
            scope["error"] = "Please Provide Valid Bearer Token"

        return await self.inner(scope, receive, send)


jwt_auth_middleware = lambda inner: JWTAuthMiddleware(AuthMiddlewareStack(inner))
