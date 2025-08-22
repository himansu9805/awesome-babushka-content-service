"""Routes for the user posts related operations."""

from commons.authentication.models import CurrentUser
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from content_service.db.schemas import PostCreate
from content_service.services import posts
from content_service.utils.commons import api_auth

posts_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=([Depends(api_auth.authenticate)]),
)
service = posts.PostService()


@posts_router.post("/create")
async def create_post(
    post: PostCreate,
    current_user: CurrentUser = Depends(api_auth.authenticate),
) -> JSONResponse:
    """Create a new post.

    ### Args:
    - **post** (`PostCreate`): The post details to be created.

    ### Returns:
    - **JSONResponse**: Response message indicating success or failure.
    """
    return await service.create_post(current_user, post)


@posts_router.get("/list")
async def get_posts(
    author: str = None,
    post_id: str = None,
) -> JSONResponse:
    """Get posts by filter.

    ### Args:
    - **author** (`str`, optional): The username of the author to filter posts.
    - **post_id** (`str`, optional): The ID of the post to retrieve.

    ### Returns:
    - **JSONResponse**: Response containing the list of posts.
    """
    filters = {}
    if author:
        filters["author"] = author
    if post_id:
        filters["post_id"] = post_id
    return await service.get_posts(filters)


@posts_router.delete("/delete/{post_id}")
async def delete_post(post_id: str) -> JSONResponse:
    """Delete a post by ID.

    ### Args:
    - **post_id** (`str`): The ID of the post to be deleted.

    ### Returns:
    - **JSONResponse**: Response message indicating success or failure.
    """
    return await service.delete_post(post_id)
