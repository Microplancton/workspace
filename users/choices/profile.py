# -*- coding: utf-8 -*-

from django.db import models


class ActivityChoices(models.TextChoices):
    GET_PASSWORDS = 'get_passwords', 'получение паролей'
    GEN_PASSWORD = 'gen_password', 'генерация пароля'
