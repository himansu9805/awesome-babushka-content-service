"""GraphQL queries for fetching posts."""

from typing import List, Optional

import strawberry

from content_service.graphql.types.post_type import PostType
from content_service.services.posts import PostService

post_service = PostService()


@strawberry.type
class Query:
    @strawberry.field
    async def post(
        self, author: Optional[str] = None, post_id: Optional[str] = None
    ) -> Optional[PostType]:
        """Return list of posts filtered by optional author or post_id.

        This resolver reuses the existing PostService to fetch posts from the
        DB and converts the JSONResponse payload into GraphQL types.
        """
        filters = {}
        if author:
            filters["author"] = author
        if post_id:
            filters["post_id"] = post_id

        post = await post_service.get_post(filters)
        return PostType(**post) if post else None

    @strawberry.field
    async def posts(
        self, author: Optional[str] = None, post_id: Optional[str] = None
    ) -> List[PostType]:
        """Return list of posts filtered by optional author or post_id.

        This resolver reuses the existing PostService to fetch posts from the
        DB and converts the JSONResponse payload into GraphQL types.
        """
        filters = {}
        if author:
            filters["author"] = author
        if post_id:
            filters["post_id"] = post_id

        posts = await post_service.get_posts(filters)
        return [PostType(**post) for post in posts]
