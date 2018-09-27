from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime


class Connection(models.Model):
    auth_user = models.CharField(max_length=20, primary_key=True)
    auth_pass = models.CharField(max_length=200)
    host_assets = models.CharField(max_length=200)
    host_api = models.CharField(max_length=200)
    last_update_time = models.DateTimeField(null=True)

    def __str__(self):
        return "{}@{}".format(self.auth_user, self.host_api)


class KoboData(models.Model):
    auth_user = models.ForeignKey(Connection, on_delete=models.CASCADE, blank=True, null=True)
    dataset_id = models.BigIntegerField(null=True)
    dataset_uuid = models.TextField(primary_key=True)
    dataset_owner = models.TextField(null=True)
    tags = ArrayField(models.TextField(null=True), null=True)
    dataset_name = models.TextField(null=True)
    dataset_year = models.IntegerField(null=True)
    last_submission_time = models.DateTimeField(null=True)
    last_checked_time = models.DateTimeField(null=True)
    last_update_time = models.DateTimeField(default=datetime.now, editable=False)
    kobo_managed = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Kobo form'
        verbose_name_plural = 'Kobo forms'

    def __str__(self):
        return "{} ({} - {})".format(self.dataset_name, self.dataset_owner,  self.dataset_year)

    def is_uptodate(self):
        if self.last_submission_time is None:
            return "No submissions"
        elif self.last_update_time is None:
            return "Never updated"
        elif self.last_update_time >= self.last_submission_time:
            return "Up to date"
        else:
            return "Out of date"
