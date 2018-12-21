from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Connection(models.Model):
    auth_user = models.CharField(max_length=20, primary_key=True)
    auth_pass = models.CharField(max_length=200)
    host_assets = models.CharField(max_length=200)
    host_api = models.CharField(max_length=200)
    last_update_time = models.DateTimeField(default=datetime.now, editable=False)

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
    last_checked_time = models.DateTimeField(default=datetime.now)
    last_update_time = models.DateTimeField(null=True, editable=False)
    kobo_managed = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Kobo form'
        verbose_name_plural = 'Kobo forms'

    def __str__(self):
        #return "{} ({} - {})".format(self.dataset_name, self.dataset_owner,  self.dataset_year)
        return self.dataset_name

    def is_uptodate(self):
        if self.last_submission_time is None:
            return "No submissions"
        elif self.last_update_time is None:
            return "Never updated"
        elif self.last_update_time >= self.last_submission_time:
            return "Up to date"
        else:
            return "Out of date"


class KoboUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # surveys = ArrayField(models.ForeignKey(KoboData, on_delete=models.CASCADE, null=True), null=True)
    surveys = models.ManyToManyField(KoboData)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_kobouser(sender, instance, created, **kwargs):
    if created:
        KoboUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_kobouser(sender, instance, **kwargs):
    instance.kobouser.save()

