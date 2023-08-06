from __future__ import print_function

from django.contrib import admin
from django.db import connections
from django.contrib.admin import SimpleListFilter

from database_deadlock.models import Deadlock


class DeadlockAdmin(admin.ModelAdmin):

    list_display = (
        'blocked_pid',
        'blocked_user',
        'blocked_query',
        'blocking_pid',
        'blocking_user',
        'blocking_query',
    )
    list_filter = (
    )
    search_fields = (
    )
    readonly_fields = (
        'id',
        'blocked_pid',
        'blocked_user',
        'blocked_query',
        'blocking_pid',
        'blocking_user',
        'blocking_query',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(DeadlockAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        return readonly_fields + [f.name for f in self.model._meta.fields if f.name not in readonly_fields]


admin.site.register(Deadlock, DeadlockAdmin)
