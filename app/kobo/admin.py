from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Connection, KoboData
from .resources import KoboDataFromFileResource, KoboDataFromKoboResource
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import tablib
from django import forms


def sync_connection(queryset):
    now = datetime.now()

    for connection in queryset:

        dataset = tablib.Dataset().load(get_kobo_forms(connection))

        kobodata_resource = KoboDataFromKoboResource()
        kobodata_resource.connection = connection
        result = kobodata_resource.import_data(dataset, raise_errors=True, dry_run=True)
        if not result.has_errors():
            kobodata_resource.import_data(dataset, dry_run=False)

            # mark missing forms on kobo as legancy - don't delete!
            update = {"auth_user": None, "kobo_managed": False}
            KoboData.objects.filter(auth_user=connection.auth_user).filter(last_checked_time__lt=now).update(**update)

        else:
            raise forms.ValidationError("Import failed!")

        connection.last_update_time = datetime.now()
        connection.save()


def get_kobo_forms(connection):
        """
        Get metadata for Kobo form
        :param connection:
        :return:
        """
        host = connection.host_api.strip()
        auth_user = connection.auth_user.strip()
        auth_passwd = connection.auth_pass.strip()
        url = "{}/{}?format=json".format(host, "forms")
        r = requests.get(url, auth=HTTPBasicAuth(auth_user, auth_passwd))
        return r.text  # json.loads(r.text)


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    """
    Admin class for Connections
    """
    list_display = ['auth_user', 'host_assets', 'last_update_time']
    ordering = ['auth_user']

    def sync(self, request, queryset):
        """
        Add action to fetch latest data from Kobo
        :param request:
        :param queryset:
        :return:
        """

        sync_connection(queryset)

        self.message_user(request, "Data successfully updated")

    actions = [sync]
    sync.short_description = "Sync data"

@admin.register(KoboData)
class KoboDataAdmin(ImportExportModelAdmin):
    list_display = ['dataset_name', 'dataset_year', 'tags', 'dataset_owner', 'last_submission_time', 'last_update_time', 'last_checked_time', 'kobo_managed']
    ordering = ['dataset_owner', 'dataset_name', 'dataset_year']
    resource_class = KoboDataFromFileResource
