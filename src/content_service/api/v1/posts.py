"""Routes for the user posts related operations."""

from typing import Optional

from commons.authentication.models import CurrentUser
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from content_service.db.schemas import PostCreateRequest
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
    post: PostCreateRequest,
    current_user: CurrentUser = Depends(api_auth.authenticate),
) -> JSONResponse:
    """Create a new post.

    ### Args:
    - **post** (`PostCreate`): The post details to be created.

    ### Returns:
    - **JSONResponse**: Response message indicating success or failure.
    """
    created = await service.create_post(current_user, post)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Post created successfully", "post": created},
    )


@posts_router.get("/list")
async def get_posts(
    author: Optional[str] = None,
    post_id: Optional[str] = None,
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
    posts_list = await service.get_posts(filters)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"posts": posts_list}
    )


@posts_router.delete("/delete/{post_id}")
async def delete_post(post_id: str) -> JSONResponse:
    """Delete a post by ID.

    ### Args:
    - **post_id** (`str`): The ID of the post to be deleted.

    ### Returns:
    - **JSONResponse**: Response message indicating success or failure.
    """
    result = await service.delete_post(post_id)
    # If deletion succeeded, provide a confirmation message
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Post deleted successfully", **result},
    )
