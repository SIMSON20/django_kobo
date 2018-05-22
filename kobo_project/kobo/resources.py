from import_export import resources
from .models import KoboData
from datetime import datetime
from import_export.fields import Field
import requests
from requests.auth import HTTPBasicAuth
import json


class KoboDataFromFileResource(resources.ModelResource):
    class Meta:
        model = KoboData
        import_id_fields = ('dataset_uuid',)


class KoboDataFromKoboResource(resources.ModelResource):
    """
    Resource for import Kobo Data directly from the Kobo API
    Existing data will be overwritten with new data
    Data no longer available on Kobo will be delete after import
    """

    start_time = datetime.now()
    connection = None
    dataset_id = Field(attribute='dataset_id', column_name='formid')
    dataset_uuid = Field(attribute='dataset_uuid', column_name='id_string')
    dataset_name = Field(attribute='dataset_name', column_name='title')
    dataset_year = Field(attribute='dataset_year', column_name='dataset_year')
    dataset_owner = Field(attribute='dataset_owner', column_name='dataset_owner')
    auth_user = Field(attribute='auth_user', column_name='auth_user')
    last_submission_time = Field(attribute='last_submission_time', column_name='last_submission_time')
    last_update_time = Field(attribute='last_update_time', column_name='last_update_time')
    tags = Field(attribute='tags', column_name='tags')

    class Meta:
        model = KoboData
        import_id_fields = ('dataset_uuid',)

    def before_import_row(self, row, **kwargs):
        row["dataset_year"] = row["date_created"][0:4]
        row["dataset_owner"] = row["owner"][40:].split('?')[0]
        #if row["last_submission_time"] is not None:
        #    row["last_submission_time"] =  datetime.strptime(row["last_submission_time"], '%Y-%m-%dT%H:%M:%S.%fZ')
        #else:
        #    return None
        row["last_update_time"] = datetime.now()
        row["auth_user"] = self.connection
        row["tags"] = self.get_kobo_assets(self.connection, row["id_string"])["tag_string"].split(",")

    @staticmethod
    def get_kobo_assets(connection, dataset_uuid):
        """
        Connect to Kobo Assets API and fetch data for selected form
        :param connection:
        :param dataset_uuid:
        :return:
        """
        host = connection.host_assets.strip()
        auth_user = connection.auth_user.strip()
        auth_passwd = connection.auth_pass.strip()
        url = "{}{}/?format=json".format(host, dataset_uuid)
        r = requests.get(url, auth=HTTPBasicAuth(auth_user, auth_passwd))
        return json.loads(r.text)

    def after_save_instance(self, instance, using_transactions, dry_run):
        """
        Delete not updated data after instance was saved
        :param instance:
        :param using_transactions:
        :param dry_run:
        :return:
        """
        pass
        #if not dry_run:
        #    queryset = self.get_queryset()
        #    q = queryset.objects.filter(last_update_time__smallerthan=self.start_time)
        #    q.delete()

