from import_export import resources
from .models import KoboData
from datetime import datetime
from import_export.fields import Field
import requests
from requests.auth import HTTPBasicAuth
import json


class KoboDataResource(resources.ModelResource):
    """
    Resource for import Kobo Data directly from the Kobo API
    Existing data will be overwritten with new data
    Data no longer available on Kobo will be delete after import
    """

    def __init__(self):
        """
        Map fields from Kobo API to table
        Set start time to find out later which data were updated
        Set connection
        """
        self.start_time = datetime.now()
        self.connection = None
        self.dataset_id = Field(column_name='formid')
        self.dataset_uuid = Field(column_name='id_string')
        self.dataset_name = Field(column_name='title')
        self.dataset_year = Field(column_name='date_created')
        self.last_submission_time = Field(column_name='last_submission_time')

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

    def dehydrate_auth_user(self, kobodata):
        """
        Get user name from connection
        :param kobodata:
        :return:
        """
        return self.connection.auth_user

    @staticmethod
    def dehydrate_dataset_owner(kobodata):
        """
        Extract dataset owner from kobo hyperlink
        :param kobodata:
        :return:
        """
        return kobodata.owner[40:].split('?')[0]

    @staticmethod
    def dehydrate_dataset_year(kobodata):
        """
        Extract year from created date timestamp
        :param kobodata:
        :return:
        """
        return kobodata.date_created[0:4]

    @staticmethod
    def dehydrate_last_submission_time(kobodata):
        """
        Convert last submission time to datetime object
        :param kobodata:
        :return:
        """
        if kobodata.last_submission_time is not None:
           return datetime.strptime(kobodata.last_submission_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            return None

    @staticmethod
    def dehydrate_last_update_time(kobodata):
        """
        Set last update time to now
        :param kobodata:
        :return:
        """
        return datetime.now()

    def dehydrate_tags(self, kobodata):
        """
        Fetch tags from Kobo form
        :param kobodata:
        :return:
        """
        return self.get_kobo_assets(self.connection, kobodata.id_string)["tag_string"].split(",")

    def after_save_instance(self, instance, using_transactions, dry_run):
        """
        Delete not updated data after instance was saved
        :param instance:
        :param using_transactions:
        :param dry_run:
        :return:
        """
        if not dry_run:
            queryset = self.get_queryset()
            q = queryset.objects.filter(last_update_time__smallerthan=self.start_time)
            q.delete()

    class Meta:
        model = KoboData
