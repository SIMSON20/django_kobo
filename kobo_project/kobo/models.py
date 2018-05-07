from django.db import models


class Connection(models.Model):
    auth_user = models.CharField(max_length=20 , primary_key=True)
    auth_pass = models.CharField(max_length=200)
    host_assets = models.CharField(max_length=200)
    host_api = models.CharField(max_length=200)

    def __str__(self):
        return "{}@{}".format(self.auth_user, self.host_api)