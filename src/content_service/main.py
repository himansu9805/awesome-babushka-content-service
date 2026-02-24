"""Main module for the auth service."""

import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from content_service.api.v1.posts import posts_router
from content_service.utils.commons import print_config
from content_service.utils.minio_client import init_minio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(api: FastAPI):
    """Lifespan method of FastAPI."""
    print_config()
    init_minio()
    yield


api = FastAPI(title="Content Service", version="0.1.0", lifespan=lifespan)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Content-Type", "Authorization"],
    expose_headers=["Content-Type"],
    max_age=3600,
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
