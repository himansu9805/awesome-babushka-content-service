"""Service for handling authentication."""

import httpx
import uuid
import logging
from fastapi import Request
from bs4 import BeautifulSoup

from commons.authentication.models import CurrentUser
from commons.database import MongoConnect
from fastapi import HTTPException, status, UploadFile
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError

from content_service.core.config import settings
from content_service.db.models import Post
from content_service.db.schemas import PostItem, SortOrder, LinkPreviewResult
from content_service.utils.minio_client import s3_client

logger = logging.getLogger(__name__)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB


class PostService:
    """Post service class."""

    def __init__(self):
        """Initialize the PostService class."""

        self.mongo_connection = MongoConnect(
            settings.MONGO_URI, settings.DB_NAME
        )

    def __del__(self):
        """Close the MongoDB connection."""
        self.mongo_connection.close()

    def _extract_meta(self, soup: BeautifulSoup, names: list[str]) -> str:
        """Extract meta content from the HTML soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.
            names (list[str]): List of meta tag names to search for.

        Returns:
            str: The content of the first matching meta tag, or an empty string
            if no matching tag is found.
        """
        for name in names:
            tag = soup.find("meta", property=name) or soup.find(
                "meta", attrs={"name": name}
            )
            if tag and tag.get("content"):
                return str(tag["content"]).strip()
        return ""

    async def create_post(
        self,
        request: Request,
        current_user: CurrentUser,
        content: str,
        images: list[UploadFile] | None = None,
    ) -> JSONResponse:
        """Create a new post.

        Args:
            request (Request): Request object.
            current_user (CurrentUser): The current authenticated user.
            content (str): The post content.
            images (list[UploadFil]e): The image files that is sent with
                content.

        Returns:
            JSONResponse: Response message indicating success or failure.

        Raises:
            HTTPException: If the post already exists or if there is an
                error during creation.
        """
        try:
            image_urls = []
            if images:
                for image in images:
                    if image.content_type not in ALLOWED_TYPES:
                        raise HTTPException(
                            status_code=400, detail="Invalid image type."
                        )

                    data = await image.read()
                    if len(data) > MAX_SIZE:
                        raise HTTPException(
                            status_code=400, detail="Image exceeds 5MB limit."
                        )

                    file_key = (
                        f"posts/{current_user.username}/{uuid.uuid4().hex}_"
                        f"{image.filename}"
                    )
                    s3_client.put_object(
                        Bucket=settings.MINIO_BUCKET,
                        Key=file_key,
                        Body=data,
                        ContentType=image.content_type,
                    )
                    image_urls.append(
                        f"{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET}"
                        f"/{file_key}"
                    )

            new_post = Post(
                content=content,
                image_urls=image_urls if image_urls else None,
                author=current_user.username or "unknown",
                user_client=request.headers.get("User-Agent", "unknown"),
            )
            self.mongo_connection.get_collection(
                settings.POSTS_COLLECTION
            ).insert_one(new_post.model_dump())
        except DuplicateKeyError:
            logger.warning("Post with ID %s already exists", new_post.post_id)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Post already exists",
            )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            logger.error("Error creating post: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            ) from e
        logger.info("Post created successfully with ID %s", new_post.post_id)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Post created successfully"},
        )

    async def get_posts(
        self, filters: dict, sort_order: SortOrder
    ) -> list[PostItem]:
        """Get posts by filter.

        Args:
            filters (dict): The filter criteria for retrieving posts.
            sort_order (SortOrder): The order in which posts should be
                returned.

        Returns:
            A list of posts.

        Raises:
            HTTPException: If the post does not exist or if there is an
                error during retrieval.
        """
        try:
            results = []
            posts = (
                self.mongo_connection.get_collection(settings.POSTS_COLLECTION)
                .find(filters, {"_id": 0})
                .sort(
                    {"updated_at": -1 if sort_order == SortOrder.LATEST else 1}
                )
            )
            results = [PostItem(**post) for post in posts]
            if len(results) == 0:
                logger.warning(
                    "No posts found for the given filter: %s", filters
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No posts found for the given filter",
                )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            logger.error("Error retrieving posts: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            ) from e
        logger.info(
            "%s posts retrieved successfully for filters: %s",
            len(results),
            filters,
        )
        return results

    async def delete_post(self, post_id: str) -> JSONResponse:
        """Delete a post by ID.

        Args:
            post_id (str): The ID of the post to be deleted.

        Returns:
            JSONResponse: Response message indicating success or failure.

        Raises:
            HTTPException: If the post does not exist or if there is an
                error during deletion.
        """
        try:
            result = self.mongo_connection.get_collection(
                settings.POSTS_COLLECTION
            ).delete_one({"post_id": post_id})
            if result.deleted_count == 0:
                logger.warning("Post %s not found for deletion", post_id)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found",
                )
        except Exception as e:
            logger.error("Error deleting post %s: %s", post_id, e)
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting the post",
            )
        logger.info("Post %s deleted successfully", post_id)
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={"message": "Post deleted successfully"},
        )

    async def fetch_link_preview(self, url: str) -> LinkPreviewResult:
        """Fetch link preview for a given URL.

        Args:
            url (str): The URL for which the preview needs to be generated.

        Returns:
            LinkPreviewResult: The preview result for the given URL.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; AwesomeBabushkaBot/1.0)"
        }

        async with httpx.AsyncClient(
            follow_redirects=True, timeout=8.0
        ) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = (
            self._extract_meta(soup, ["og:title", "twitter:title"])
            or (
                soup.find("title").get_text(strip=True)
                if soup.find("title")
                else ""
            )
            or url
        )

        description = self._extract_meta(
            soup, ["og:description", "twitter:description", "description"]
        )

        parsed_url = httpx.URL(url)
        origin = f"{parsed_url.scheme}://{parsed_url.host}"
        favicon = f"https://www.google.com/s2/favicons?domain={origin}&sz=32"

        return LinkPreviewResult(
            url=url,
            title=title,
            description=description,
            favicon=favicon,
        )
