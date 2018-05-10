from django.contrib import admin
from .models import Connection, KoboData
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['auth_user', 'host_assets']
    ordering = ['auth_user']

    def sync(self, request, queryset):

        #onnections = queryset.values()
        for connection in queryset:

            # delete all records for selected connection
            KoboData.objects.filter(auth_user=connection.auth_user).delete()

            # fetch all forms
            forms = self.get_kobo_forms(connection)

            # fetch all asssets and data for selected forms and write to table
            for form in forms:
                KoboData.objects.create(
                                   auth_user = connection,
                                   dataset_id= int(form['formid']),
                                   dataset_uuid=form['id_string'],
                                   dataset_owner = form['owner'][40:],
                                   tags = self.get_kobo_assets(connection, form['id_string'])["tag_string"].split(","),
                                   dataset_name = form['title'],
                                   dataset_year = int(form['date_created'][0:4]),
                                   last_submission_time = datetime.strptime(form['last_submission_time'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                   dataset = self.get_kobo_data(connection, form["formid"])
                                   )

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
    def get_kobo_assets(connection, dataset_uuid):

        host = connection.host_assets.strip()
        auth_user = connection.auth_user.strip()
        auth_passwd = connection.auth_pass.strip()
        url = "{}{}/?format=json".format(host, dataset_uuid)

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
    list_display = ['dataset_name', 'dataset_year', 'tags', 'dataset_owner', 'last_submission_time']
    ordering = ['dataset_owner', 'dataset_name', 'dataset_year']

admin.site.register(Connection, ConnectionAdmin)
admin.site.register(KoboData, KoboDataAdmin)