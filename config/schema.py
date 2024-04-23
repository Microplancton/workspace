# -*- coding: utf-8 -*-

import graphql_jwt
from graphene import ObjectType, Schema

from users.schema import Mutation as UsersMutation


class Query(
    ObjectType
):
    pass

class Mutation(
    UsersMutation,
    ObjectType,
):
    verify_token = graphql_jwt.Verify.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()

# query потом
schema = Schema(mutation=Mutation)
