# -*- coding: utf-8 -*-

from graphene import ObjectType
from graphene_django.types import DjangoObjectType

from .profile import Mutation as ProfileMutation


class Mutation(
    ProfileMutation,
    ObjectType,
):
    pass
