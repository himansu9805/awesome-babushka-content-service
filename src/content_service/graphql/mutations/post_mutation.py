import strawberry
from strawberry import Info

from content_service.db.schemas import PostCreateRequest
from content_service.graphql.types.post_type import PostType
from content_service.services.posts import PostService

post_service = PostService()


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_post(self, content: str, info: Info) -> PostType:
        """Create a new post."""
        created_post = await post_service.create_post(
            current_user=info.context["current_user"],
            creation_request=PostCreateRequest(content=content),
        )
        return PostType(**created_post)

    @strawberry.mutation
    async def delete_post(self, post_id: str) -> bool:
        """Delete a post."""
        result = await post_service.delete_post(post_id=post_id)
        return True if result.get("deleted_count", 0) > 0 else False
