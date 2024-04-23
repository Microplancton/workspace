
# -*- coding: utf-8 -*-

from datetime import date
import jwt
from typing import Optional

from graphql_jwt.utils import jwt_payload

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.db.transaction import atomic
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from users.models import Profile

from users.choices import ActivityChoices
from utils.date_helper import get_current_date


validate_username = ASCIIUsernameValidator()


@atomic
def create_profile(
    username: str, email: str, password: str, repeat_password: str,
) -> Profile:
    """
    Сервис по созданию профиля пользователя

    :param username: Имя пользователя
    :param email: Email пользователя
    :param password: Пароль
    :param repeat_password: Повторный пароль

    :returns: Возвращает объект users.Profile
    """

    if repeat_password != password:
        raise Exception('Пароли не совпадают')

    validate_password(password=password)

    if User.objects.filter(username=username).exists():
        raise Exception('Пользователь с таким именем уже существует')

    validate_email(email)
    validate_username(username)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    return Profile.objects.create(user=user)


@atomic
def gen_jwt_token(profile: Profile) -> str:
    """
    Сервис генерации jwt токена для пользователя.

    :param profile: Объект профиля

    :returns: Возвращает сгенерированный токен
    """

    payload = jwt_payload(profile.user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    return token


@atomic
def update_profile(user_id: int,
            new_username: Optional[str] = None,
            new_email: Optional[str] = None,
            new_first_name: Optional[str] = None,
            new_last_name: Optional[str] = None) -> Profile:
    """
    Функция для обновления профиля пользователя.

    :param user_id: ID пользователя, профиль которого нужно обновить.
    :param new_username: Новое имя пользователя.
    :param new_email: Новая электронная почта.
    :param new_first_name: Новое имя пользователя.
    :param new_last_name: Новая фамилия пользователя.

    :return: Обновленный профиль пользователя.
    """

    profile = Profile.objects.get(user_id=user_id)

    if new_email:
        validate_email(new_email)

    if new_username:
        validate_username(new_username)

    # Проверяем, что новое имя пользователя не занято другим пользователем
    if new_username and User.objects.exclude(
            id=profile.user.id).filter(username=new_username).exists():
        raise ValidationError("Пользователь с таким именем уже существует")

    # Проверяем, что новая электронная почта не занята другим пользователем
    if new_email and User.objects.exclude(
            id=profile.user.id).filter(email=new_email).exists():
        raise ValidationError("Пользователь с такой электронной почтой уже существует")

    # FIXME: переписать на более правильную логику
    # Обновляем поля профиля, если они были переданы
    if new_username:
        profile.user.username = new_username
        profile.user.save()
    if new_email:
        profile.user.email = new_email
    if new_first_name:
        profile.first_name = new_first_name
    if new_last_name:
        profile.last_name = new_last_name

    # Сохраняем изменения
    profile.user.save()
    profile.save()

    return profile


@atomic
def update_password(
        user_id: int,
        old_password: str,
        new_password: str,
        repeat_password: str
        ) -> Profile:
    """
    Функция апдейта пароля у пользователя

    :param user_id: ID пользователя
    :param old_password: текущий пароль пользователя
    :param new_password: Новый пароль
    :param repeat_password: повторения пароля

    :return: Обновленный пароль
    """

    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        raise ValueError('Пользователь не найден.')

    if profile.user.check_password(old_password):
        raise ValueError('Старый пароль неверен.')

    if new_password != repeat_password:
        raise ValueError('Пароли не совпадают.')

    validate_password(new_password)

    profile.user.set_password(new_password)
    profile.user.save()

    return profile
