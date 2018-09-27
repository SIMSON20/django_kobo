from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin
from django.contrib.gis.admin import GeoModelAdmin
from .models import AME, Answer, AnswerGPS, AnswerGS, AnswerHHMembers, AnswerNR, Price, BNSForm, BNSFormPrice
from .resources import AMEFromFileResource, AnswerFromFileResource, AnswerFromKoboResource, AnswerGPSFromKoboResource, \
                            AnswerGPSFromFileResource, AnswerGSFromFileResource, AnswerGSFromKoboResource, \
                            AnswerHHMembersFromFileResource, AnswerHHMembersFromKoboResource, \
                            AnswerNRFromFileResource, AnswerNRFromKoboResource, PriceFromKoboResource
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import tablib
import copy


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


@admin.register(AME)
class AMEAdmin(ImportExportModelAdmin):
    list_display = ['age', 'gender', 'ame', 'calories']
    resource_class = AMEFromFileResource


@admin.register(AnswerGPS)
class AnswerGPSAdmin(GeoModelAdmin, ImportExportModelAdmin):
    list_display = ['answer', 'lat', 'long', 'geom', 'last_update']
    resource_class = AnswerGPSFromFileResource



class AnswerGPSInline(admin.StackedInline):
    model = AnswerGPS

# TODO get base map to show
# admin.site.register(AnswerGPS, GeoModelAdmin)


@admin.register(AnswerGS)
class AnswerGSAdmin(ImportExportModelAdmin):
    list_display = ['answer', 'gs', 'necessary', 'have', 'quantity', 'last_update']
    resource_class = AnswerGSFromFileResource


class AnswerGSInline(admin.StackedInline):
    model = AnswerGS
    extra = 1


@admin.register(AnswerHHMembers)
class AnswerHHMembersAdmin(ImportExportModelAdmin):
    list_display = ['answer', 'gender', 'birth', 'ethnicity', 'head', 'last_update']
    resource_class = AnswerHHMembersFromFileResource


class AnswerHHMembersInline(admin.StackedInline):
    model = AnswerHHMembers
    extra = 1


@admin.register(AnswerNR)
class AnswerNRAdmin(ImportExportModelAdmin):
    list_display = ['answer', 'nr', 'nr_collect', 'last_update']
    resource_class = AnswerNRFromFileResource


class AnswerNRInline(admin.StackedInline):
    model = AnswerNR
    extra = 1


@admin.register(Answer)
class AnswerAdmin(ImportExportModelAdmin):
    """
    Admin class for Connections
    """
    list_display = ['dataset_uuid', 'answer_id', 'landscape', 'surveyor', 'participant', 'arrival', 'district',
                    'village', 'hh_type_control', 'hh_type_org_benef', 'hh_type_other_benef', 'hh_id', 'livelihood_1',
                    'livelihood_2', 'livelihood_3', 'livelihood_4', 'benef_project', 'explain_project', 'know_pa',
                    'benef_pa', 'explain_benef_pa', 'bns_plus', 'survey_date', 'last_update']
    inlines = [AnswerGPSInline, AnswerGSInline, AnswerHHMembersInline, AnswerNRInline]
    resource_class = AnswerFromFileResource


@admin.register(Price)
class PriceAdmin(ImportExportModelAdmin):
    """
    Admin class for Connections
    """
    list_display = ['dataset_uuid', 'village', 'gs', 'price']


@admin.register(BNSForm)
class BNSFormAdmin(ImportExportModelAdmin):
    """
    Admin class for BNS FormsConnections
    """
    list_display = ['dataset_name', 'dataset_year', 'dataset_owner', 'dataset_uuid',
                    'last_submission_time', 'last_update_time', 'last_checked_time', 'kobo_managed']


    def sync(self, request, queryset):
        """
        Add action to fetch latest data from Kobo
        :param request:
        :param queryset:
        :return:
        """

        for form in queryset:
            # TODO: make sure to remove archived forms from queryset

            dataset = get_kobo_data(form.auth_user, form.dataset_id)
            self._sync_bns(dataset, form, request)
            form.last_update_time = datetime.now()
            form.save()


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
            i = 1
            row = dict()
            row["answer_id"] = data_row["_uuid"]
            row["gender"] = data_row["gender_head"]
            row["birth"] = data_row["birth_head"]
            if "ethnicity_head" in data_row.keys():
                row["ethnicity"] = data_row["ethnicity_head"]
            else:
                row["ethnicity"] = None
            row["head"] = True
            row["seq"] = i
            new_dataset.append(row)

            if data_row["hh_members"] is not None:
                for member in data_row["hh_members"]:
                    i += 1
                    row = dict()
                    row["answer_id"] = data_row["_uuid"]
                    if "gender" in member.keys():
                        row["gender"] = member["hh_members/gender"]
                    else:
                        row["gender"] = None

                    if "birth" in member.keys():
                        row["birth"] = member["hh_members/birth"]
                    else:
                        row["birth"] = None

                    if "hh_members/ethnicity" in member.keys():
                        row["ethnicity"] = member["hh_members/ethnicity"]
                    else:
                        row["ethnicity"] = None

                    row["head"] = False
                    row["seq"] = i
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

    actions = [sync]
    sync.short_description = "Sync data"


@admin.register(BNSFormPrice)
class BNSFormPriceAdmin(ImportExportModelAdmin):
    """
    Admin class for BNS Price Forms
    """
    list_display = ['dataset_name', 'related_dataset', 'dataset_year', 'dataset_owner', 'dataset_uuid',
                    'last_submission_time', 'last_update_time', 'last_checked_time', 'kobo_managed']

    def sync(self, request, queryset):
        """
        Add action to fetch latest data from Kobo
        :param request:
        :param queryset:
        :return:
        """

        for form in queryset:
            # TODO: make sure to remove archived forms from queryset

            dataset = get_kobo_data(form.auth_user, form.dataset_id)
            self._sync_bns_price(dataset, form, request)
            form.last_update_time = datetime.now()
            form.save()

    def _sync_bns_price(self, dataset, form, request):
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
            if "good" in data_row.keys():
                for gs in data_row["good"]:
                    if "good/name" in gs.keys() and "good/price" in gs.keys():
                        row = dict()
                        row["dataset_uuid"] = form.related_uuid
                        row["surveyor"] = data_row["surveyor"]
                        row["village"] = data_row["village"]
                        row["gs"] = gs["good/name"]
                        row["price"] = gs["good/price"]
                        new_dataset.append(row)

            elif "group_prices" in data_row.keys():
                for gs in data_row["group_prices"]:
                    if "group_prices/good_name" in gs.keys() and "group_prices/good_price" in gs.keys():
                        row = dict()
                        row["dataset_uuid"] = form.related_uuid
                        row["surveyor"] = data_row["surveyor"]
                        row["village"] = data_row["group_info/village"]
                        row["gs"] = gs["group_prices/good_name"]
                        row["price"] = gs["group_prices/good_price"]
                        new_dataset.append(row)

        dataset = tablib.Dataset().load(json.dumps(new_dataset, sort_keys=True))

        # Update AnswerGPS table
        result = price_resource.import_data(dataset, raise_errors=True, dry_run=True)
        if not result.has_errors():
            price_resource.import_data(dataset, dry_run=False)

            # Delete not updated records
            Price.objects.filter(dataset_uuid=form.related_uuid).filter(last_update__lt=now).delete()

            self.message_user(request, "Successfully updated {} prices for form {}".format(len(dataset),
                                                                                                    form.dataset_name))
        else:
            self.message_user(request, "Failed to updated prices for form {}".format(form.dataset_name),
                              level=messages.ERROR)

    actions = [sync]
    sync.short_description = "Sync data"