# -*- coding: utf-8 -*-

from datetime import datetime, date

from django.utils.timezone import get_current_timezone


def get_current_date() -> date:
    """
    Функция которая возвращает текущую дату

    :returns: Объект datetime.date
    """

    now = datetime.now().replace(tzinfo=get_current_timezone())
    return now.date()
