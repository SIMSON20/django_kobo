from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField


class Connection(models.Model):
    auth_user = models.CharField(max_length=20 , primary_key=True)
    auth_pass = models.CharField(max_length=200)
    host_assets = models.CharField(max_length=200)
    host_api = models.CharField(max_length=200)

    def __str__(self):
        return "{}@{}".format(self.auth_user, self.host_api)


class KoboData(models.Model):
    auth_user = models.ForeignKey(
        Connection,
        on_delete=models.CASCADE,
    )
    dataset_id = models.BigIntegerField(null=True)
    dataset_uuid = models.TextField(null=True)
    dataset_owner = models.TextField(null=True)
    tags = ArrayField(models.TextField(null=True))
    dataset_name = models.TextField(null=True)
    dataset_year = models.IntegerField(null=True)
    last_submission_time = models.DateTimeField(null=True)
    dataset = JSONField(null=True)

    def __str__(self):
        return "{}@{}".format(self.auth_user, self.dataset_id)