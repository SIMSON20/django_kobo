from django.contrib import admin
from .models import Connection, KoboData
from .resources import KoboDataResource
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import tablib


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['auth_user', 'host_assets']
    ordering = ['auth_user']

    def sync(self, request, queryset):

        for connection in queryset:

            dataset = tablib.dict(self.get_kobo_forms(connection))

            kobodata_resource = KoboDataResource()
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


admin.site.register(Connection, ConnectionAdmin)
admin.site.register(KoboData, KoboDataAdmin)
