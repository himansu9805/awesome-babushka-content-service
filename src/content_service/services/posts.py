"""Service for handling authentication."""

import json
import logging

from commons.authentication.models import CurrentUser
from commons.database import MongoConnect
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from content_service.core.config import settings
from content_service.db.models import Post
from content_service.db.schemas import PostCreateRequest

logger = logging.getLogger(__name__)


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

    async def create_post(
        self, current_user: CurrentUser, creation_request: PostCreateRequest
    ) -> dict:
        """Create a new post.

        Args:
            current_user (CurrentUser): The current authenticated user.
            creation_request (PostCreateRequest): The post details to
                be created.

        Returns:
            dict: The created post data.

        Raises:
            HTTPException: If the post already exists or if there is an
                error during creation.
        """
        try:
            new_post = Post(
                content=creation_request.content,
                author=str(current_user.username),
            )
            self.mongo_connection.get_collection(
                settings.POSTS_COLLECTION
            ).insert_one(new_post.model_dump())
        except DuplicateKeyError:
            logger.warning(
                "Post with ID %s already exists",
                getattr(creation_request, "post_id", None),
            )
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
        logger.info(
            "Post created successfully with ID %s",
            getattr(new_post, "post_id", None),
        )
        # Return raw created post data
        return new_post.model_dump()

    async def get_post(self, filters: dict) -> dict:
        """Get a single post by filters.

        Args:
            filters (dict): The filter criteria for retrieving the post.

        Returns:
            dict: The post matching the filters.

        Raises:
            HTTPException: If the post does not exist or if there is an
                error during retrieval.
        """
        try:
            post = self.mongo_connection.get_collection(
                settings.POSTS_COLLECTION
            ).find_one(filters, {"_id": 0})
            if not post:
                logger.warning(
                    "Post not found for the given filter: %s", filters
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found for the given filter",
                )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            logger.error("Error retrieving post: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            ) from e
        logger.info("Post retrieved successfully for filters: %s", filters)
        # Return raw post data
        return post

    async def get_posts(self, filters: dict) -> list:
        """Get posts by filter.

        Args:
            filters (dict): The filter criteria for retrieving posts.

        Returns:
            list: The list of posts matching the filters.

        Raises:
            HTTPException: If the post does not exist or if there is an
                error during retrieval.
        """
        try:
            posts_cursor = self.mongo_connection.get_collection(
                settings.POSTS_COLLECTION
            ).find(filters, {"_id": 0})
            posts = json.loads(json.dumps(list(posts_cursor), default=str))
            if len(posts) == 0:
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
            len(posts),
            filters,
        )
        # Return raw posts list
        return posts

    async def delete_post(self, post_id: str) -> dict:
        """Delete a post by ID.

        Args:
            post_id (str): The ID of the post to be deleted.

        Returns:
            dict: Deletion result info, e.g. {"deleted_count": n}

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
        # Return raw deletion result
        return {"deleted_count": result.deleted_count}
