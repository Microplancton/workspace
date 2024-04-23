# -*- coding: utf-8 -*-


from django.db import models


class Tag(models.Model):
    """ Модель тега для пароля """
    COLOR_PICKER =[
        ('red', 'Красный'),
        ('yellow', 'Желтый'),
        ('green', 'Зеленый'),
        ('aquamarine', 'Аквомариновый'),
        ('blue', 'Синий'),
        ('purple', 'Фиолетовый'),
        ('black', 'Черный')
    ]

    owner = models.ForeignKey(
            'users.Profile',
            on_delete=models.CASCADE,
            related_name='tag_owner'
    )

    password = models.ForeignKey(
            'passwords.Password',
            on_delete=models.DO_NOTHING,
            related_name='password_tag'
    )

    tag = models.CharField(
            max_length=128,
            null=False, blank=False,
            verbose_name='тег'
    )

    color = models.CharField(
            max_length=16,
            choices=COLOR_PICKER,
            verbose_name='Цвет'
    )
