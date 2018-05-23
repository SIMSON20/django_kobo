from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Connection, KoboData
from .resources import KoboDataFromFileResource, KoboDataFromKoboResource
from bns.resources import AnswerFromKoboResource, AnswerGPSFromKoboResource
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import tablib
from django import forms


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

        for connection in queryset:

            dataset = tablib.Dataset().load(self.get_kobo_forms(connection))

            kobodata_resource = KoboDataFromKoboResource()
            kobodata_resource.connection = connection
            result = kobodata_resource.import_data(dataset, raise_errors=True, dry_run=True)
            if not result.has_errors():
                result = kobodata_resource.import_data(dataset, dry_run=False)
            else:
                raise forms.ValidationError("Import failed!")

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
        return r.text # json.loads(r.text)

    actions = [sync]
    sync.short_description = "Sync data"


@admin.register(KoboData)
class KoboDataAdmin(ImportExportModelAdmin):
    list_display = ['dataset_name', 'dataset_year', 'tags', 'dataset_owner', 'last_submission_time', 'last_update_time']
    ordering = ['dataset_owner', 'dataset_name', 'dataset_year']
    resource_class = KoboDataFromFileResource

    def sync(self, request, queryset):
        """
        Add action to fetch latest data from Kobo
        :param request:
        :param queryset:
        :return:
        """

        for form in queryset:
            #import pdb; pdb.set_trace()
            dataset = self.get_kobo_data(form.auth_user, form.dataset_id)

            # make sure every row has the same keys.
            # get all unique keys
            keys = set()
            for row in dataset:
                keys |= set(row.keys())

            # add missing keys to rows
            for row in dataset:
                key_set = set(keys)
                key_set -= set(row.keys())
                for key in key_set:
                    row[key] = None

            dataset = tablib.Dataset().load(json.dumps(dataset, sort_keys=True))

            answer_resource = AnswerFromKoboResource()
            answer_resource.form = form

            answer_gps_resource = AnswerGPSFromKoboResource()

            result = answer_resource.import_data(dataset, raise_errors=True, dry_run=True)
            if not result.has_errors():
                answer_resource.import_data(dataset, dry_run=False)
                result = answer_gps_resource.import_data(dataset, raise_errors=True, dry_run=True)
                if not result.has_errors():
                    answer_gps_resource.import_data(dataset, dry_run=False)
                else:
                    raise forms.ValidationError("Import of AnswersGPS failed!")
            else:
                raise forms.ValidationError("Import of Answers failed!")

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