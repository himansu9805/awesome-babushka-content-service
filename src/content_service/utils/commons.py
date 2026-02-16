"""Common utilities for the content service"""

import logging

from commons.authentication import ApiAuth

from content_service.core.config import settings

logger = logging.getLogger(__name__)

api_auth = ApiAuth(
    auth_url=f"{settings.AUTH_URL}/api/v1/token/validate",
    public_key=settings.JWT_PUBLIC_KEY,
    algorithm=settings.JWT_ALGORITHM,
    issuer=settings.JWT_ISSUER,
    audience=settings.JWT_AUDIENCE,
)


def print_config():
    """Print the current configuration settings."""
    logger.info("AUTH URL: %s", settings.AUTH_URL)
