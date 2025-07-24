"""Service for handling authentication."""

import json

from commons.database import MongoConnect
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError

from content_service.core.config import settings
from content_service.db.models import Post
from content_service.db.schemas import PostCreate


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

    async def create_post(self, post: PostCreate) -> JSONResponse:
        """Create a new post.

        Args:
            post (PostCreate): The post details to be created.

        Returns:
            JSONResponse: Response message indicating success or failure.

        Raises:
            HTTPException: If the post already exists or if there is an
                error during creation.
        """
        try:
            new_post = Post(content=post.content, author=post.author)
            self.mongo_connection.get_collection(
                settings.POSTS_COLLECTION
            ).insert_one(new_post.model_dump())
        except DuplicateKeyError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Post already exists",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            ) from e
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Post created successfully"},
        )

    async def get_posts(self, filters: dict) -> JSONResponse:
        """Get posts by filter.

        Args:
            filters (dict): The filter criteria for retrieving posts.

        Returns:
            JSONResponse: The posts details.

        Raises:
            HTTPException: If the post does not exist or if there is an
                error during retrieval.
        """
        try:
            posts = self.mongo_connection.get_collection(
                settings.POSTS_COLLECTION
            ).find(filters, {"_id": 0})
            posts = json.loads(json.dumps(list(posts), default=str))
            if len(posts) == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No posts found for the given filter",
                )
            return JSONResponse(status_code=status.HTTP_200_OK, content=posts)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            ) from e
