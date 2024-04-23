# -*- coding: utf-8 -*-

from typing import Union, Tuple

from datetime import datetime

from django.contrib import admin
from django.db.models import QuerySet

from django.http import HttpRequest

from users.models import Profile

class IsActiveFilter(admin.SimpleListFilter):
    title = 'Активность'
    parameter_name = 'get_is_active'

    def lookups(
        self, request: HttpRequest, queryset: QuerySet,
    ) -> Tuple[Tuple[str, str]]:
        return (
            ('yes', 'Да'),
            ('no', 'Нет'),
        )

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        value = self.value()
        if value == 'yes':
            return Profile.objects.active()
        if value == 'no':
            return Profile.objects.not_active()
        return queryset


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = (
        'get_username',
        'get_email',
        'created_at',
        'get_is_active',
        'get_last_activity',
        'first_name',
        'last_name'
    )

    readonly_fields = (
        'get_username',
        'get_email',
        'created_at',
        'get_is_active',
        'get_last_activity',
    )

    search_fields = (
        'user__username',
    )

    list_filter = (
        IsActiveFilter,
    )

    list_display = (
        'get_username',
        'get_is_active',
    )


    def get_username(self, obj: Profile) -> str:
        return obj.username
    get_username.short_description = 'Имя пользователя'

    def get_email(self, obj: Profile) -> str:
        return obj.email
    get_email.short_description = 'Email'

    # TODO: нужна оптимизация (скорее всего через annotate)
    def get_is_active(self, obj: Profile) -> str:
        return obj.is_active
    get_is_active.short_description = 'Активность'
    get_is_active.boolean = True

    def get_last_activity(self, obj: Profile) -> Union[datetime, str]:
        if last_activity := obj.last_activity:
            return last_activity.strftime('%d.%M.%Y %H:%m')
        return '-'
    get_last_activity.short_description = 'Время последней активности'

    def has_delete_permission(
        self, request: HttpRequest, obj: Profile = None,
    ) -> bool:
        return False

    def has_add_permission(self, requst: HttpRequest) -> bool:
        return False
