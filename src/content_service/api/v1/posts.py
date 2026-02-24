"""Routes for the user posts related operations."""

import httpx
from commons.authentication.models import CurrentUser
from fastapi import (
    APIRouter,
    Depends,
    Request,
    Form,
    UploadFile,
    File,
    HTTPException,
)
from fastapi.responses import JSONResponse

from content_service.db.schemas import (
    PostItem,
    SortOrder,
    LinkPreviewRequest,
    LinkPreviewResult,
)
from content_service.services import posts
from content_service.utils.commons import api_auth

posts_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=([Depends(api_auth.authenticate)]),
)
service = posts.PostService()


@posts_router.post(
    "/create",
    description=(
        "## Create a new post with the current logged in user.\n\n"
        "This endpoint creates a new post for the current logged in user. A "
        "post, as of now, has a content body and optional set of images "
        "attached with it.\n\n"
        "### Request Body:\n"
        "It is a form body with following set of fields:\n"
        "- **content** (`str`): The content of the post to be created.\n"
        "- **images** (`list[UploadFile]`, optional): Images attached with "
        "the post.\n\n"
        "### Returns:\n"
        "A `JSONResponse` message indicating success or failure."
    ),
)
async def create_post(
    request: Request,
    content: str = Form(..., min_length=1, max_length=300),
    images: list[UploadFile] = File(default=[]),
    current_user: CurrentUser = Depends(api_auth.authenticate),
) -> JSONResponse:
    """Create a new post.

    ### Args:
    - **request** (`Request`): The request object for API call.
    - **content** (`str`): The content of the post to be created.
    - **images** (`list[UploadFile]`, optional): Images attached with the post.
    - **current_user** (`CurrentUser`): Details of the current logged in user.

    ### Returns:
    - **JSONResponse**: Response message indicating success or failure.
    """
    return await service.create_post(request, current_user, content, images)


@posts_router.get("/list")
async def get_posts(
    author: str | None = None,
    post_id: str | None = None,
    sort_order: SortOrder = SortOrder.LATEST,
) -> list[PostItem]:
    """Get posts by filter.

    ### Args:
    - **author** (`str`, optional): The username of the author to filter posts.
    - **post_id** (`str`, optional): The ID of the post to retrieve.
    - **sort_order** (`SortOrder`): Sorting order

    ### Returns:
    - **JSONResponse**: Response containing the list of posts.
    """
    filters = {}
    if author:
        filters["author"] = author
    if post_id:
        filters["post_id"] = post_id
    return await service.get_posts(filters, sort_order)


@posts_router.delete("/delete/{post_id}")
async def delete_post(post_id: str) -> JSONResponse:
    """Delete a post by ID.

    ### Args:
    - **post_id** (`str`): The ID of the post to be deleted.

    ### Returns:
    - **JSONResponse**: Response message indicating success or failure.
    """
    return await service.delete_post(post_id)


@posts_router.post("/link-preview", response_model=LinkPreviewResult)
async def get_link_preview(
    body: LinkPreviewRequest,
) -> LinkPreviewResult:
    """Get link preview for a given URL.

    ### Args:
    - **body** (`LinkPreviewRequest`): The request body containing the URL.

    ### Returns:
    - **LinkPreviewResult**: The preview result for the given URL.
    """
    try:
        return await service.fetch_link_preview(str(body.url))
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Target URL returned {e.response.status_code}",
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=422, detail=f"Could not reach URL: {e}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
