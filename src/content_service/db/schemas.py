"""Models for the auth service"""

from pydantic import BaseModel
from pydantic.fields import Field


class PostCreate(BaseModel):
    """Post creation model"""

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
    author: str = Field(
        ...,
        title="Author Username",
        description="Username of the author who created the post",
        min_length=1,
        examples=["johndoe"],
    )
