"""GraphQL schema definition and setup"""

import strawberry
from commons.authentication.models import CurrentUser
from fastapi import Depends
from strawberry.fastapi import GraphQLRouter

from content_service.graphql.mutations.post_mutation import (
    Mutation as PostMutation,
)
from content_service.graphql.queries.post_queries import Query as PostQuery
from content_service.utils.commons import api_auth


async def get_context(
    current_user: CurrentUser = Depends(api_auth.authenticate),
):
    """Resolve and expose the authenticated user to GraphQL resolvers."""
    return {"current_user": current_user}


post_schema = strawberry.Schema(query=PostQuery, mutation=PostMutation)
post_graphql = GraphQLRouter(post_schema, context_getter=get_context)
