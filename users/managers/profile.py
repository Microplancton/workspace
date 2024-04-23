# -*- coding: utf-8 -*-

from datetime import timedelta

from django.db import models
from django.db.models import QuerySet
from config import settings

from utils import get_current_date

class ProfileManager(models.Manager):
    """ Менеджер для модели Profile """

    END_DATE = get_current_date()
    START_DATE = END_DATE- timedelta(days=settings.INACTIVE_USER_DAYS)

    def active(self) -> QuerySet:
        """ Возвращает queryset активных пользоватлей """

        qs =self.get_queryset()
        return qs.filter(last_activity__range=[self.START_DATE, self.END_DATE])


    def not_active(self) -> QuerySet:
        """ Возвращает queryset из не активных пользователей """

        qs = self.get_queryset()
        return qs.exclude(last_activity__range=[self.START_DATE, self.END_DATE])
