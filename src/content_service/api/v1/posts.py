"""Routes for the user posts related operations."""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from content_service.db.schemas import PostCreate
from content_service.services import posts
from content_service.utils.commons import api_auth

posts_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(api_auth.authenticate)],
)
service = posts.PostService()


@posts_router.post("")
async def create_post(post: PostCreate) -> JSONResponse:
    """Create a new post.

    ### Args:
    - post (PostCreate): The post details to be created.

    ### Returns:
    - JSONResponse: Response message indicating success or failure.
    """
    return await service.create_post(post)


@posts_router.get("")
async def get_posts(author: str = None, post_id: str = None) -> JSONResponse:
    """Get posts by filter.

    ### Args:
    - author (str, optional): The username of the author to filter posts.
    - post_id (str, optional): The ID of the post to retrieve.

    ### Returns:
    - JSONResponse: Response containing the list of posts.
    """
    filters = {}
    if author:
        filters["author"] = author
    if post_id:
        filters["post_id"] = post_id
    return await service.get_posts(filters)
