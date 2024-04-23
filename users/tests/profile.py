# -*- coding: utf-8 -*-

from graphql_relay import from_global_id
from graphene_django.utils.testing import GraphQLTestCase

from django.test import TestCase

from users.models import Profile
from users.services import create_profile


class ProfileTestCase(TestCase):
    """ TestCase для тестирования сервисов users.Profile """

    def test_create_profile(self) -> None:
        """ Тест на проверку сервиса по созданию профиля пользователя """

        # Проверка на разные пароли
        with self.assertRaises(Exception):
            create_profile(
                username='test',
                email='test@foo.ru',
                password='foo',
                repeat_password='f',
            )

        # Проверка на не валидный email
        with self.assertRaises(Exception):
            create_profile(
                username='test',
                email='test',
                password='Passw0rd33',
                repeat_password='Passw0rd33',
            )

        # Проверка на "плохой" пароль
        with self.assertRaises(Exception):
            create_profile(
                username='test',
                email='test@foo.ru',
                password='1234',
                repeat_password='1234',
            )

        # Проверка на "плохое" имя пользователя
        with self.assertRaises(Exception):
            create_profile(
                username='Алексей',
                email='test@test.com',
                password='Passw0rd33',
                repeat_password='Passw0rd33',
            )

        profile: Profile = create_profile(
            username='test',
            email='test@foo.ru',
            password='Passw0rd33',
            repeat_password='Passw0rd33',
        )

        self.assertEqual(hasattr(profile, 'user'), True)
        self.assertEqual(profile.username, 'test')
        self.assertEqual(profile.email, 'test@foo.ru')

        # Проверка на то, что такой пользователь уже существует
        with self.assertRaises(Exception):
            create_profile(
                username='test',
                email='test@foo.ru',
                password='Passw0rd33',
                repeat_password='Passw0rd33',
            )

class ProfileAPITestCase(GraphQLTestCase):
    """ TestCase для тестирования Profile API """

    REGISTER_USER_MUTATION = '''
    mutation RegisterUserMutation($input: RegisterUserMutationInput!) {
        registerUser(input: $input) {
            profile {
                id
            }
        }
    }
    '''

    GRAPHQL_URL = '/api/'

    def test_register_user_mutaion(self) -> None:
        """ Тест на проверку мутации по регистрации пользователя """

        response = self.query(
            self.REGISTER_USER_MUTATION,
            input_data={
                'username': 'test_user',
                'email': 'test@foo.ru',
                'password': 'Passw0rd33',
                'repeatPassword': 'Passw0rd33',
            },
        )

        self.assertResponseNoErrors(response)

        profile_pk = response.json()['data']['registerUser']['profile']['id']
        _, pk = from_global_id(profile_pk)
        new_profile = Profile.objects.get(pk=pk)
        self.assertEqual(new_profile.user.username, 'test_user')
