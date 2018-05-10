from import_export import resources
from .models import KoboData
from datetime import datetime
from import_export.fields import Field
import requests
from requests.auth import HTTPBasicAuth
import json


class KoboDataResource(resources.ModelResource):

    def __init__(self):
        self.start_time = datetime.now()
        self.connection = None
        self.dataset_id = Field(column_name='formid')
        self.dataset_uuid = Field(column_name='id_string')
        self.dataset_name = Field(column_name='title')
        self.dataset_year = Field(column_name='date_created')
        self.last_submission_time = Field(column_name='last_submission_time')

    @staticmethod
    def get_kobo_assets(connection, dataset_uuid):
        host = connection.host_assets.strip()
        auth_user = connection.auth_user.strip()
        auth_passwd = connection.auth_pass.strip()
        url = "{}{}/?format=json".format(host, dataset_uuid)
        r = requests.get(url, auth=HTTPBasicAuth(auth_user, auth_passwd))
        return json.loads(r.text)

    def dehydrate_auth_user(self, kobodata):
        return self.connection.auth_user

    @staticmethod
    def dehydrate_dataset_owner(kobodata):
        return kobodata.owner[40:].split('?')[0]

    @staticmethod
    def dehydrate_dataset_year(kobodata):
        return kobodata.date_created[0:4]

    @staticmethod
    def dehydrate_last_submission_time(kobodata):
        if kobodata.last_submission_time is not None:
           return datetime.strptime(kobodata.last_submission_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            return None

    @staticmethod
    def dehydrate_last_update_time(kobodata):
        return datetime.now()

    def dehydrate_tags(self, kobodata):
        return self.get_kobo_assets(self.connection, kobodata.id_string)["tag_string"].split(",")

    def after_save_instance(self, instance, using_transactions, dry_run):
        if not dry_run:
            queryset = self.get_queryset()
            q = queryset.objects.filter(last_update_time__smallerthan=self.start_time)
            q.delete()

    class Meta:
        model = KoboData
