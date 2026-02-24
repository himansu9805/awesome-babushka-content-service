"""Database models for the content service"""

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel
from pydantic.fields import Field


class Post(BaseModel):
    """Post model"""

    post_id: str = Field(
        default_factory=lambda: str(uuid4().hex),
        title="Post ID",
        description="Unique identifier for the post",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    content: str = Field(
        ...,
        title="Post Content",
        description="Content of the post",
        min_length=1,
        max_length=5000,
        examples=[
            "This is the content of the first post.",
            "This is the content of the second post.",
        ],
    )
    image_urls: list[str] | None = Field(
        default=None,
        title="Image URLs",
        description="URLs of the uploaded images stored in object store",
    )
    author: str = Field(
        ...,
        title="Author Username",
        description="Username of the author who created the post",
        min_length=1,
        examples=["johndoe"],
    )
    user_client: str = Field(
        ...,
        title="User Client",
        description="Information of the client that sends the request",
        examples=[
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ],
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Creation Timestamp",
        description="Timestamp when the post was created",
        examples=[datetime.now(timezone.utc)],
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        title="Update Timestamp",
        description="Timestamp when the post was last updated",
        examples=[datetime.now(timezone.utc)],
    )
