"""Common utilities for the content service"""

from commons.authentication import ApiAuth

from content_service.core.config import settings

api_auth = ApiAuth(
    auth_url=settings.AUTH_URL,
    disable_auth=settings.DISABLE_AUTH,
)
