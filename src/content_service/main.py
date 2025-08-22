"""Main module for the auth service."""

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from content_service.api.v1.posts import posts_router
from content_service.utils.commons import print_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api = FastAPI(
    title="Content Service",
    version="0.1.0",
    on_startup=[print_config],
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(posts_router, prefix="/api/v1")


@api.get("/", include_in_schema=False)
async def root():
    """Redirect to API documentation."""
    return RedirectResponse(url="/docs")


def main():
    """Run the FastAPI application."""
    uvicorn.run(api)


if __name__ == "__main__":
    main()
