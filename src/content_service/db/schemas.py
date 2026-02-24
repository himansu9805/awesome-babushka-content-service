"""Models for the auth service"""

from enum import Enum

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, HttpUrl
from pydantic.fields import Field


class SortOrder(Enum):
    LATEST = "latest"
    OLDEST = "oldest"


class PostCreate(BaseModel):
    """Post creation request model."""

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


class UserPlatformInfo(BaseModel):
    """User platform information model."""

    application: str = Field(
        "Unknown",
        title="Client Application Name",
        description="Name of the application from where post was created",
        examples=["Edge", "Chrome", "Firefox", "Safari"],
    )
    os: str = Field(
        "Unknown",
        title="Client Operating System",
        description="Operating system on which client is installed",
        examples=["Windows", "Mac OS X", "Linux", "Android", "iOS"],
    )
    device: str = Field(
        "desktop",
        title="Client Device Type",
        description="Type of device from where request has been made",
        examples=["desktop", "mobile", "tablet"],
    )


class PostItem(BaseModel):
    """Post Item model."""

    post_id: str = Field(
        ...,
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
    user_platform: UserPlatformInfo | None = Field(
        None,
        title="User Platform Info",
        description="Information of the user client that created the post",
    )
    user_client: str = Field(
        ...,
        title="User Client",
        description="Information of the client that sends the request",
        examples=[
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ],
        exclude=True,
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

    def model_post_init(self, context: Any) -> None:
        super().model_post_init(context)
        platform = {
            "application": "Unknown",
            "os": "Unknown",
            "device": "desktop",
        }

        # Detect OS
        if "Windows" in self.user_client:
            platform["os"] = "Windows"
        elif "Mac OS X" in self.user_client:
            platform["os"] = "Mac OS X"
        elif "Android" in self.user_client:
            platform["os"] = "Android"
            platform["device"] = "mobile"
        elif "iPhone" in self.user_client:
            platform["os"] = "iOS"
            platform["device"] = "mobile"
        elif "iPad" in self.user_client:
            platform["os"] = "iOS"
            platform["device"] = "tablet"
        elif "Linux" in self.user_client:
            platform["os"] = "Linux"

        # Detect Browser
        if "Edg/" in self.user_client:
            platform["application"] = "Edge"
        elif "Chrome/" in self.user_client:
            platform["application"] = "Chrome"
        elif "Firefox/" in self.user_client:
            platform["application"] = "Firefox"
        elif "Safari/" in self.user_client and "Version/" in self.user_client:
            platform["application"] = "Safari"

        self.user_platform = UserPlatformInfo(**platform)


class LinkPreviewRequest(BaseModel, frozen=True):
    """Link preview request model."""

    url: HttpUrl = Field(
        ...,
        title="URL",
        description="The URL for which the preview needs to be generated",
        examples=["https://www.example.com"],
    )


class LinkPreviewResult(BaseModel, frozen=True):
    """Link preview result model."""

    url: str = Field(
        ...,
        title="URL",
        description="The URL for which the preview is generated",
        examples=["https://www.example.com"],
    )
    title: str = Field(
        ...,
        title="Title",
        description="The title of the linked page",
        examples=["Example Domain"],
    )
    description: str = Field(
        ...,
        title="Description",
        description="A brief description of the linked page",
        examples=[
            "This domain is for use in illustrative examples in documents."
        ],
    )
    favicon: str = Field(
        ...,
        title="Favicon URL",
        description="URL of the favicon of the linked page",
        examples=["https://www.example.com/favicon.ico"],
    )
