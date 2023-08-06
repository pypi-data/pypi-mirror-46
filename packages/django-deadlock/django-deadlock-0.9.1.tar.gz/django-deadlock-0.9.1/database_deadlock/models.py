from __future__ import print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Deadlock(models.Model):

    id = models.CharField(max_length=255, primary_key=True, editable=False)

    blocked_pid = models.CharField(max_length=500, editable=False)
    blocked_user = models.CharField(max_length=500, editable=False)
    blocked_query = models.TextField(editable=False)

    blocking_pid = models.CharField(max_length=500, editable=False)
    blocking_user = models.CharField(max_length=500, editable=False)
    blocking_query = models.TextField(editable=False)

    class Meta:
        managed = False
        verbose_name = _('deadlock')
        db_table = 'database_deadlock_deadlock'
