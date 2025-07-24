""" Middleware for the FastAPI application. """

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)


def setup_middlewares(app):
    """Set up middlewares for the FastAPI application.

    Args:
        app (FastAPI): FastAPI application instance

    Returns:
        None
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def limit_auth_routes(request: Request, call_next):
        """Rate limiter middleware.

        Args:
            request (Request): Request object
            call_next (Callable): Next middleware function

        Returns:
            Response
        """
        if request.url.path in ["/login", "/register"]:
            return await limiter.limit("5/minute")(call_next)(request)
        return await call_next(request)
