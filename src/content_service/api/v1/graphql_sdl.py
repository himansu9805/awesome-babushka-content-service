"""Routes for the GraphQL SDL."""

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from content_service.graphql.schema import post_schema
from content_service.utils.commons import api_auth

sdl_router = APIRouter(
    prefix="/graphql/sdl",
    tags=["GraphQL SDL"],
    dependencies=([Depends(api_auth.authenticate)]),
)


@sdl_router.get("/post", response_class=PlainTextResponse)
async def create_post() -> str:
    """Return the GraphQL schema in SDL (GraphQL Schema Definition Language)
    for the post service.
    """
    return post_schema.as_str()
