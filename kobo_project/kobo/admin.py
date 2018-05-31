from django.contrib import admin, messages
# from django.contrib.messages import constants as messages
from import_export.admin import ImportExportModelAdmin
from .models import Connection, KoboData
from .resources import KoboDataFromFileResource, KoboDataFromKoboResource
from bns.resources import AnswerFromKoboResource, AnswerGPSFromKoboResource, \
                            AnswerGSFromKoboResource, AnswerHHMembersFromKoboResource, \
                            AnswerNRFromKoboResource, PriceFromKoboResource
from bns.models import Answer, AnswerGPS, AnswerGS, AnswerHHMembers, AnswerNR, Price
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
                kobodata_resource.import_data(dataset, dry_run=False)
            else:
                raise forms.ValidationError("Import failed!")

            connection.last_update_time = datetime.now()
            connection.save()

        self.message_user(request, "Data successfully updated")

    @staticmethod
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
            dataset = self.get_kobo_data(form.auth_user, form.dataset_id)

            if "bns" in form.tags:
                self._sync_bns(dataset, form, request)

            elif "bnsprice" in form.tags:
                tag = form.tags
                tag.remove('bnsprice')
                #import pdb; pdb.set_trace()
                if len(tag) > 1:
                    self.message_user(request,
                                      "Cannot sync {}. Dataset UUID is ambiguous. Too many tags.".format(form.dataset_name),
                                      level=messages.ERROR)
                else:
                    self._sync_bns_price(dataset, tag[0], form, request)

    def _sync_bns(self, dataset, form, request):
        """
        Syncs selected BNS data with Kobo
        :param dataset:
        :param form:
        :param request:
        :return:
        """
        dataset = self._normalize_data(dataset)

        answer_resource = AnswerFromKoboResource()
        answer_gps_resource = AnswerGPSFromKoboResource()
        answer_gs_resource = AnswerGSFromKoboResource()
        answer_hh_members_resource = AnswerHHMembersFromKoboResource()
        answer_nr_resource = AnswerNRFromKoboResource()

        answer_resource.form = form

        now = datetime.now()

        # Update main Answer table
        result = answer_resource.import_data(dataset, raise_errors=True, dry_run=True)
        if not result.has_errors():
            answer_resource.import_data(dataset, dry_run=False)

            # Delete not updated records
            Answer.objects.filter(dataset_uuid=form.dataset_uuid).filter(last_update__lt=now).delete()

            self.message_user(request,
                              "Successfully updated {} answers for form {}".format(len(dataset), form.dataset_name))

            # Update AnswerGPS table
            result = answer_gps_resource.import_data(dataset, raise_errors=True, dry_run=True)
            if not result.has_errors():
                answer_gps_resource.import_data(dataset, dry_run=False)

                # Delete not updated records
                AnswerGPS.objects.filter(answer__dataset_uuid=form.dataset_uuid).filter(last_update__lt=now).delete()

                self.message_user(request, "Successfully updated {} GPS coordinates for form {}".format(len(dataset),
                                                                                                        form.dataset_name))
            else:
                self.message_user(request, "Failed to updated GPS coordinates for form {}".format(form.dataset_name),
                                  level=messages.ERROR)

            # Update AnswerGS table
            gs_dataset = self._extract_gs(dataset.dict)

            result = answer_gs_resource.import_data(gs_dataset, raise_errors=True, dry_run=True)
            if not result.has_errors():
                answer_gs_resource.import_data(gs_dataset, dry_run=False)

                # Delete not updated records
                AnswerGS.objects.filter(answer__dataset_uuid=form.dataset_uuid).filter(last_update__lt=now).delete()

                self.message_user(request, "Successfully updated {} Goods & Service entries for form {}".format(len(gs_dataset),
                                                                                                        form.dataset_name))
            else:
                self.message_user(request, "Failed to updated Goods & Service entries for form {}".format(form.dataset_name),
                                  level=messages.ERROR)

            # Update HH Member table
            hh_member_dataset = self._extract_hh_members(dataset.dict)

            result = answer_hh_members_resource.import_data(hh_member_dataset, raise_errors=True, dry_run=True)
            if not result.has_errors():
                answer_hh_members_resource.import_data(hh_member_dataset, dry_run=False)

                # Delete not updated records
                AnswerHHMembers.objects.filter(answer__dataset_uuid=form.dataset_uuid).filter(last_update__lt=now).delete()

                self.message_user(request,
                                  "Successfully updated {} household member entries for form {}".format(len(hh_member_dataset),
                                                                                                       form.dataset_name))
            else:
                self.message_user(request,
                                  "Failed to updated household member entries for form {}".format(form.dataset_name),
                                  level=messages.ERROR)

            # Update NR table
            nr_dataset = self._extract_nr(dataset.dict)

            result = answer_nr_resource.import_data(nr_dataset, raise_errors=True, dry_run=True)
            if not result.has_errors():
                answer_nr_resource.import_data(nr_dataset, dry_run=False)

                # Delete not updated records
                AnswerNR.objects.filter(answer__dataset_uuid=form.dataset_uuid).filter(last_update__lt=now).delete()

                self.message_user(request,
                                  "Successfully updated {} natural resource entries for form {}".format(len(nr_dataset),
                                                                                                       form.dataset_name))
            else:
                self.message_user(request,
                                  "Failed to updated natural resource entries for form {}".format(form.dataset_name),
                                  level=messages.ERROR)

        else:
            self.message_user(request, "Failed to updated answers for form {}".format(form.dataset_name),
                              level=messages.ERROR)
            # raise forms.ValidationError("Import of Answers failed!")

    def _sync_bns_price(self, dataset, dataset_uuid, form, request):
        """
        Sync Prices
        :param dataset:
        :param dataset_uuid:
        :param form:
        :param request:
        :return:
        """
        price_resource = PriceFromKoboResource()

        now = datetime.now()

        new_dataset = list()
        for data_row in dataset:

            for gs in data_row["good"]:
                row = dict()
                row["dataset_uuid"] = dataset_uuid
                row["village"] = data_row["village"]
                row["gs"] = gs["good/name"]
                row["price"] = gs["good/price"]

                new_dataset.append(row)

        dataset = tablib.Dataset().load(json.dumps(new_dataset, sort_keys=True))

        # Update AnswerGPS table
        result = price_resource.import_data(dataset, raise_errors=True, dry_run=True)
        if not result.has_errors():
            price_resource.import_data(dataset, dry_run=False)

            # Delete not updated records
            Price.objects.filter(kobodata__dataset_uuid=form.dataset_uuid).filter(last_update__lt=now).delete()

            self.message_user(request, "Successfully updated {} prices for form {}".format(len(dataset),
                                                                                                    form.dataset_name))
        else:
            self.message_user(request, "Failed to updated prices for form {}".format(form.dataset_name),
                              level=messages.ERROR)


    @staticmethod
    def _normalize_data(dataset):
        """
        Expects a list of dictionaries with key value pairs
        Returns a tablib dataset
        :param dataset:
        :return:
        """

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

        return tablib.Dataset().load(json.dumps(dataset, sort_keys=True))

    @staticmethod
    def _extract_gs(dataset):
        """
        Read Kobo data and extract Good and Services answers
        Convert table and write each GS answer in a seperate row
        :param dataset:
        :return:
        """

        matrix_group_prefix = "bns_matrix"
        new_dataset = list()
        for data_row in dataset:
            answer_id = data_row["_uuid"]
            filtered_row = {k: v for (k, v) in data_row.items() if matrix_group_prefix in k}
            gs = set([k.split('/')[0][len(matrix_group_prefix)+1:] for k in filtered_row.keys()])

            for item in gs:
                row = dict()
                row["answer_id"] = answer_id
                row["gs"] = item
                row["have"] = True if filtered_row[
                                          "{0}_{1}/{0}_{1}_{2}".format(matrix_group_prefix, item, "possess")] == 'yes' else False
                row["necessary"] = True if filtered_row["{0}_{1}/{0}_{1}_{2}".format(matrix_group_prefix,item,
                                                                                                     "necessary")] == 'yes' else False
                if "{0}_{1}/{0}_{1}_{2}".format(matrix_group_prefix,item, "number") not in filtered_row or not row["have"]:
                    row["quantity"] = None
                else:
                    row["quantity"] = filtered_row["{0}_{1}/{0}_{1}_{2}".format(matrix_group_prefix, item, "number")]

                new_dataset.append(row)

        return tablib.Dataset().load(json.dumps(new_dataset, sort_keys=True))


    @staticmethod
    def _extract_hh_members(dataset):
        """
        Read Kobo data and extract Household Members from answers
        Convert table and write each HH Member in a seperate row
        :param dataset:
        :return:
        """

        new_dataset = list()

        for data_row in dataset:

            row = dict()
            row["answer_id"] = data_row["_uuid"]
            row["gender"] = data_row["gender_head"]
            row["birth"] = data_row["birth_head"]
            row["ethnicity"] = data_row["ethnicity_head"]
            row["head"] = True
            new_dataset.append(row)

            if data_row["hh_members"] is not None:
                for member in data_row["hh_members"]:
                    row = dict()
                    row["answer_id"] = data_row["_uuid"]
                    row["gender"] = member["hh_members/gender"]
                    row["birth"] = member["hh_members/birth"]
                    row["ethnicity"] = member["hh_members/ethnicity"]
                    row["head"] = False
                    new_dataset.append(row)

        return tablib.Dataset().load(json.dumps(new_dataset, sort_keys=True))

    @staticmethod
    def _extract_nr(dataset):
        """
        Read Kobo data and extract Good and Services answers
        Convert table and write each GS answer in a seperate row
        :param dataset:
        :return:
        """

        nr_prefix = "nr"
        new_dataset = list()
        for data_row in dataset:
            answer_id = data_row["_uuid"]
            filtered_row = {k: v for (k, v) in data_row.items() if k[:3] == "{}/".format(nr_prefix)}

            for key in filtered_row.keys():
                row = dict()
                row["answer_id"] = answer_id
                row["nr"] = key.split('/')[1]
                row["nr_collect"] = filtered_row[key]
                new_dataset.append(row)

        return tablib.Dataset().load(json.dumps(new_dataset, sort_keys=True))

    @staticmethod
    def get_kobo_data(connection, dataset_id):
        """
        Get data for Kobo form
        :param connection:
        :param dataset_id:
        :return:
        """
        host = connection.host_api.strip()
        auth_user = connection.auth_user.strip()
        auth_passwd = connection.auth_pass.strip()
        url = "{}/{}/{}?format=json".format(host, "data", str(dataset_id))
        r = requests.get(url, auth=HTTPBasicAuth(auth_user, auth_passwd))
        return json.loads(r.text)

    actions = [sync]
    sync.short_description = "Sync data"