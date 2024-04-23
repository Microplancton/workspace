# -*- coding: utf-8 -*-


from django.db import models
from django.core.validators import MinLengthValidator


class Password(models.Model):
    """ Модель пароля """
    
    owner = models.ForeignKey(
            'users.Profile',
            on_delete=models.CASCADE,
            related_name='tag_owner'
    )

    title = models.CharField(
            max_length=256,
            null=True, blank=True,
            verbose_name='Имя пароля'
    )

    url = models.URLField(
            verbose_name='URL',
            null=True, blank=True
    )

    login = models.CharField(
            max_length=128,
            verbose_name='Логин',
            null=True, blank=True
    )

    passwords = models.CharField(
             verbose_name='Зашифрованный пароль',
             max_length=1024
    )
