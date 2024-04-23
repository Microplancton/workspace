# -*- coding: utf-8 -*-

from typing import Any, Dict

from django.core.exceptions import ValidationError
from graphql.error import GraphQLError

import graphene
from graphene import relay, ObjectType
from graphene_django.types import DjangoObjectType

from users.models import Profile
from users.services import (create_profile, gen_jwt_token,
                            update_profile, update_password)



class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        interfaces = (relay.Node,)
        # exclude_fields = ('password',)

    user_id = graphene.Int()
    username = graphene.String()
    email = graphene.String()


class RegisterUserMutation(relay.ClientIDMutation):
    """
    Мутация для регистрации пользователя.
    """

    profile = graphene.Field(ProfileNode)
    token = graphene.String()

    class Input:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        repeat_password = graphene.String(required=True)

    @staticmethod
    def mutate_and_get_payload(
        root: Any,
        info: graphene.ResolveInfo,
        **input: Dict[str, Any]
                        ):
        """
        Создаёт новый профиль пользователя и генерирует JWT
         токен для аутентификации.

        :param root: Корневой объект, который передаётся в мутацию.
         Обычно не используется.
        :param info: Информация о запросе,
         включая контекст выполнения и аргументы.
        :param input: Словарь с данными для создания профиля,
         включая имя пользователя, электронную почту,
         пароль и повторение пароля.

        :return: Объект мутации с созданным профилем и JWT токеном.
        """

        try:
            profile = create_profile(
                username=input['username'],
                email=input['email'],
                password=input['password'],
                repeat_password=input['repeat_password'],
            )
        except ValidationError as errors:
            # Собираем все ошибки в список
            error_list = [str(error) for error in errors]
            # Поднимаем исключение с сообщением, содержащим все ошибки
            raise GraphQLError(message='\n'.join(error_list))
        token = gen_jwt_token(profile=profile)

        return RegisterUserMutation(profile=profile, token=token)


class UpdateProfileMutation(relay.ClientIDMutation):
    """ Мутация обновления пользователя """

    profile = graphene.Field(ProfileNode)

    class Input:
        user_id = graphene.Int(required=True)
        username = graphene.String(required=False)
        email = graphene.String(required=False)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)

    @staticmethod
    def mutate_and_get_payload(
        root: Any,
        info: graphene.ResolveInfo,
        **input: Dict[str, Any]
    ):
        """
        Редактирование профиля.

        :param root: Корневой объект, который передаётся в мутацию.
         Обычно не используется.
        :param info: Информация о запросе,
         включая контекст выполнения и аргументы.
        :param input: Словарь с данными для редактирования профиля.

        :return:
        """

        try:
            profile = update_profile(
                user_id=input['user_id'],
                new_username=input['username'],
                new_email=input['email'],
                new_first_name=input['first_name'],
                new_last_name=input['last_name']
            )
        except ValidationError as errors:
            # Собираем все ошибки в список
            error_list = [str(error) for error in errors]
            # Поднимаем исключение с сообщением, содержащим все ошибки
            raise GraphQLError(message='\n'.join(error_list))

        return UpdateProfileMutation(profile=profile)



class UpdatePasswordMutation(relay.ClientIDMutation):
    """ Мутация для апдейта пароля у пользователя """

    profile = graphene.Field(ProfileNode)
    token = graphene.String()

    class Input:
        user_id = graphene.Int(required=True)
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)
        repeat_password = graphene.String(required=True)

    @staticmethod
    def mutate_and_get_payload(
        root: Any,
        info: graphene.ResolveInfo,
        **input: Dict[str, Any]
                        ):
        """
        Обновляет пароль пользователя и отдает токен для аутентификации

        :param root: Корневой объект, который передаётся в мутацию.
         Обычно не используется.
        :param info: Информация о запросе,
         включая контекст выполнения и аргументы.
        :param input: Словарь с данными для создания профиля,
         включая имя пользователя, электронную почту,
         пароль и повторение пароля.

        :return: Объект мутации с профилем и JWT токеном.
        """

        try:
            profile = update_password(
                user_id=input['user_id'],
                old_password=input['old_password'],
                new_password=input['new_password'],
                repeat_password=input['repeat_password']
            )
        except ValidationError as errors:
            # Собираем все ошибки в список
            error_list = [str(error) for error in errors]
            # Поднимаем исключение с сообщением, содержащим все ошибки
            raise GraphQLError(message='\n'.join(error_list))
        token = gen_jwt_token(profile=profile)

        return RegisterUserMutation(profile=profile, token=token)




class Mutation(ObjectType):
    register_user = RegisterUserMutation.Field()
    update_profile = UpdateProfileMutation.Field()
    update_password = UpdatePasswordMutation.Field()
