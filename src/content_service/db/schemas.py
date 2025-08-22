"""Models for the auth service"""

from uuid import uuid4

from pydantic import BaseModel
from pydantic.fields import Field


class PostCreate(BaseModel):
    """Post creation model"""

    post_id: str = Field(
        None,
        title="Post ID",
        description="Unique identifier for the post",
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
    author: str = Field(
        ...,
        title="Author Username",
        description="Username of the author who created the post",
        min_length=1,
        examples=["johndoe"],
    )

    def model_post_init(self, context):
        super().model_post_init(context)
        self.post_id = str(uuid4())
