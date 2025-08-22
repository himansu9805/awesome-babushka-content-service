"""GraphQL type definitions for Post."""

import strawberry


@strawberry.type
class PostType:
    post_id: strawberry.ID = strawberry.field(name="post_id")
    content: str
    author: str
    created_at: str = strawberry.field(name="created_at")
    updated_at: str = strawberry.field(name="updated_at")
