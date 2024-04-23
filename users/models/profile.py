# -*- coding: utf-8 -*-

from typing import Optional
from datetime import datetime

from django.db import models
from config import settings
from django.utils.timezone import get_current_timezone

from users.managers import ProfileManager
from utils import get_current_date


class Profile(models.Model):
    """ Модель профиля пользователя """

    user = models.OneToOneField(
        'auth.User', on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    created_at = models.DateField(
        auto_now_add=True, verbose_name='Пользователь создан'
    )

    first_name = models.CharField(
        max_length=256,
        null=True, blank=True,
        verbose_name = "Имя")

    last_name = models.CharField(
        max_length=256,
        null=True, blank=True,
        verbose_name='Фамилия'
    )

    objects = ProfileManager()

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'


    @property
    def is_active(self) -> bool:
        """
        Проверка активности пользователей.
        Если последняя активность была больше чем 182 дня назад -
        пользователь не активен.
        """

        if not self.last_activity:
            return False

        now = get_current_date()
        delta_in_days = (now - self.last_activity.date()).days

        if delta_in_days >= settings.INACTIVE_USER_DAYS:
            return False
        return True


    @property
    def last_activity(self) -> Optional[datetime]:
        """ Время последней активности пользователя """

        if hasattr(self, 'activities'):
            if last_activity := self.activities.last():
                return last_activity.date.replace(tzinfo=get_current_timezone())
        return None


    @property
    def username(self) -> str:
        """ Возвращаем username пользователя """
        return self.user.username

    @property
    def email(self) -> str:
        """ Возвращаем email пользователя """
        return self.user.email

    def __str__(self) -> str:
        return f'{self.username}'
