from django.contrib import admin
from .models import Connection, KoboData
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
from import_export import resources
from import_export.fields import Field
import tablib


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['auth_user', 'host_assets']
    ordering = ['auth_user']

    def sync(self, request, queryset):

        for connection in queryset:

            dataset = tablib.dict(self.get_kobo_forms(connection))

            kobodata_resource = resources.modelresource_factory(model=KoboData)
            kobodata_resource.connection = connection
            result = kobodata_resource.import_data(dataset, dry_run=True)
            if not result.has_errors():
                result = kobodata_resource.import_data(dataset, dry_run=False)
            else:
                pass

            connection.last_update_time = datetime.now()
            connection.save()

        self.message_user(request, "Data successfully updated")

    @staticmethod
    def get_kobo_forms(connection):
        host = connection.host_api.strip()
        auth_user = connection.auth_user.strip()
        auth_passwd = connection.auth_pass.strip()
        url = "{}/{}?format=json".format(host, "forms")
        r = requests.get(url, auth=HTTPBasicAuth(auth_user, auth_passwd))
        return json.loads(r.text)

    @staticmethod
    def get_kobo_data(connection, dataset_id):
        host = connection.host_api.strip()
        auth_user = connection.auth_user.strip()
        auth_passwd = connection.auth_pass.strip()
        url = "{}/{}/{}?format=json".format(host, "data", str(dataset_id))
        r = requests.get(url, auth=HTTPBasicAuth(auth_user, auth_passwd))
        return json.loads(r.text)

    actions = [sync]
    sync.short_description = "Sync data"


class KoboDataAdmin(admin.ModelAdmin):
    list_display = ['dataset_name', 'dataset_year', 'tags', 'dataset_owner', 'last_submission_time', 'last_update_time']
    ordering = ['dataset_owner', 'dataset_name', 'dataset_year']


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
        queryset = self.get_queryset()
        q = queryset.objects.filter(last_update_time__smallerthan=self.start_time)
        q.delete()

    class Meta:
        model = KoboData


admin.site.register(Connection, ConnectionAdmin)
admin.site.register(KoboData, KoboDataAdmin)
