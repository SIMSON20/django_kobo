from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin
from django.contrib.gis.admin import GeoModelAdmin
from .models import AME, Answer, AnswerGPS, AnswerGS, AnswerHHMembers, AnswerNR, Price, BNSForm, BNSFormPrice, District, Landscape
from .resources import AMEFromFileResource, AnswerFromFileResource, AnswerFromKoboResource, AnswerGPSFromKoboResource, \
                            AnswerGPSFromFileResource, AnswerGSFromFileResource, AnswerGSFromKoboResource, \
                            AnswerHHMembersFromFileResource, AnswerHHMembersFromKoboResource, \
                            AnswerNRFromFileResource, AnswerNRFromKoboResource, PriceFromKoboResource

import json
from datetime import datetime
import tablib
from kobo.utils import get_kobo_data, normalize_data
from .filters import AnswerLandscapeFilter, AnswerSurveyFilter, AnswerVillageFilter, \
                    SubAnswerLandscapeFilter, SubAnswerSurveyFilter, SubAnswerVillageFilter, \
                    PriceAnswerLandscapeFilter, PriceAnswerVillageFilter


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
        gs = set([k.split('/')[0][len(matrix_group_prefix) + 1:] for k in filtered_row.keys()])

        for item in gs:
            row = dict()
            row["answer_id"] = answer_id
            row["gs"] = item
            row["have"] = True if filtered_row[
                                      "{0}_{1}/{0}_{1}_{2}".format(matrix_group_prefix, item,
                                                                   "possess")] == 'yes' else False
            row["necessary"] = True if filtered_row["{0}_{1}/{0}_{1}_{2}".format(matrix_group_prefix, item,
                                                                                 "necessary")] == 'yes' else False
            if "{0}_{1}/{0}_{1}_{2}".format(matrix_group_prefix, item, "number") not in filtered_row or not row["have"]:
                row["quantity"] = None
            else:
                row["quantity"] = filtered_row["{0}_{1}/{0}_{1}_{2}".format(matrix_group_prefix, item, "number")]

            new_dataset.append(row)

    return tablib.Dataset().load(json.dumps(new_dataset, sort_keys=True))


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



def sync_answers(dataset, dataset_uuid, now=datetime.now()):

    # Update main Answer table
    answer_resource = AnswerFromKoboResource()
    result = answer_resource.import_data(dataset, raise_errors=True, dry_run=True)
    if not result.has_errors():
        answer_resource.import_data(dataset, dry_run=False)

        # Delete not updated records
        Answer.objects.filter(dataset_uuid=dataset_uuid).filter(last_update__lt=now).delete()

        return {"status": "success", "count": len(dataset)}

    else:
        return {"status": "error"}


def sync_answersgps(dataset, dataset_uuid, now=datetime.now()):

    # Update AnswerGPS table

    answer_gps_resource = AnswerGPSFromKoboResource()
    result = answer_gps_resource.import_data(dataset, raise_errors=True, dry_run=True)

    if not result.has_errors():
        answer_gps_resource.import_data(dataset, dry_run=False)

        # Delete not updated records
        AnswerGPS.objects.filter(answer__dataset_uuid=dataset_uuid).filter(last_update__lt=now).delete()

        return {"status": "success", "count": len(dataset)}

    else:
        return {"status": "error"}


def sync_answersgs(dataset, dataset_uuid, now=datetime.now()):
    # Update AnswerGS table

    answer_gs_resource = AnswerGSFromKoboResource()
    gs_dataset = _extract_gs(dataset.dict)

    result = answer_gs_resource.import_data(gs_dataset, raise_errors=True, dry_run=True)
    if not result.has_errors():
        answer_gs_resource.import_data(gs_dataset, dry_run=False)

        # Delete not updated records
        AnswerGS.objects.filter(answer__dataset_uuid=dataset_uuid).filter(last_update__lt=now).delete()

        return {"status": "success", "count": len(gs_dataset)}

    else:
        return {"status": "error"}


def sync_answershhmembers(dataset, dataset_uuid, now=datetime.now()):
    # Update HH Member table

    answer_hh_members_resource = AnswerHHMembersFromKoboResource()
    hh_member_dataset = _extract_hh_members(dataset.dict)

    result = answer_hh_members_resource.import_data(hh_member_dataset, raise_errors=True, dry_run=True)
    if not result.has_errors():
        answer_hh_members_resource.import_data(hh_member_dataset, dry_run=False)

        # Delete not updated records
        AnswerHHMembers.objects.filter(answer__dataset_uuid=dataset_uuid).filter(last_update__lt=now).delete()

        return {"status": "success", "count": len(hh_member_dataset)}

    else:
        return {"status": "error"}


def sync_answersnr(dataset, dataset_uuid, now=datetime.now()):
    # Update NR table
    answer_nr_resource = AnswerNRFromKoboResource()
    nr_dataset = _extract_nr(dataset.dict)

    result = answer_nr_resource.import_data(nr_dataset, raise_errors=True, dry_run=True)
    if not result.has_errors():
        answer_nr_resource.import_data(nr_dataset, dry_run=False)

        # Delete not updated records
        AnswerNR.objects.filter(answer__dataset_uuid=dataset_uuid).filter(last_update__lt=now).delete()

        return {"status": "success", "count": len(nr_dataset)}

    else:
        return {"status": "error"}


def sync_price(dataset, dataset_uuid, now=datetime.now()):
    price_resource = PriceFromKoboResource()
    new_dataset = list()
    for data_row in dataset:
        if "good" in data_row.keys():
            for gs in data_row["good"]:
                if "good/name" in gs.keys() and "good/price" in gs.keys():
                    row = dict()
                    row["dataset_uuid"] = dataset_uuid
                    row["surveyor"] = data_row["surveyor"]
                    row["village"] = data_row["village"]
                    row["gs"] = gs["good/name"]
                    row["price"] = gs["good/price"]
                    new_dataset.append(row)

        elif "group_prices" in data_row.keys():
            for gs in data_row["group_prices"]:
                if "group_prices/good_name" in gs.keys() and "group_prices/good_price" in gs.keys():
                    row = dict()
                    row["dataset_uuid"] = dataset_uuid
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
        Price.objects.filter(dataset_uuid=dataset_uuid).filter(last_update__lt=now).delete()

        return {"status": "success", "count": len(dataset)}

    else:
        return {"status": "error"}


@admin.register(AME)
class AMEAdmin(ImportExportModelAdmin):
    list_display = ['age', 'gender', 'ame', 'calories']
    resource_class = AMEFromFileResource


@admin.register(AnswerGPS)
class AnswerGPSAdmin(GeoModelAdmin, ImportExportModelAdmin):
    list_display = ['answer', 'lat', 'long', 'geom', 'last_update']
    resource_class = AnswerGPSFromFileResource
    list_filter = (SubAnswerLandscapeFilter, SubAnswerSurveyFilter, SubAnswerVillageFilter,)

    def get_queryset(self, request):
        # let's make sure that staff can only see their own data
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            surveys = [s.dataset_uuid for s in request.user.kobouser.surveys.all()]
            qs = qs.filter(answer__dataset_uuid_id__in=surveys)

        return qs


class AnswerGPSInline(admin.StackedInline):
    model = AnswerGPS


@admin.register(AnswerGS)
class AnswerGSAdmin(ImportExportModelAdmin):
    list_display = ['answer', 'gs', 'necessary', 'have', 'quantity', 'last_update']
    resource_class = AnswerGSFromFileResource
    list_filter = (SubAnswerLandscapeFilter, SubAnswerSurveyFilter, SubAnswerVillageFilter,)

    def get_queryset(self, request):
        # let's make sure that staff can only see their own data
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            surveys = [s.dataset_uuid for s in request.user.kobouser.surveys.all()]
            qs = qs.filter(answer__dataset_uuid_id__in=surveys)

        return qs

class AnswerGSInline(admin.StackedInline):
    model = AnswerGS
    extra = 1


@admin.register(AnswerHHMembers)
class AnswerHHMembersAdmin(ImportExportModelAdmin):
    list_display = ['answer', 'gender', 'birth', 'ethnicity', 'head', 'last_update']
    resource_class = AnswerHHMembersFromFileResource
    list_filter = (SubAnswerLandscapeFilter, SubAnswerSurveyFilter, SubAnswerVillageFilter,)

    def get_queryset(self, request):
        # let's make sure that staff can only see their own data
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            surveys = [s.dataset_uuid for s in request.user.kobouser.surveys.all()]
            qs = qs.filter(answer__dataset_uuid_id__in=surveys)

        return qs


class AnswerHHMembersInline(admin.StackedInline):
    model = AnswerHHMembers
    extra = 1


@admin.register(AnswerNR)
class AnswerNRAdmin(ImportExportModelAdmin):
    list_display = ['answer', 'nr', 'nr_collect', 'last_update']
    resource_class = AnswerNRFromFileResource
    list_filter = (SubAnswerLandscapeFilter, SubAnswerSurveyFilter, SubAnswerVillageFilter,)

    def get_queryset(self, request):
        # let's make sure that staff can only see their own data
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            surveys = [s.dataset_uuid for s in request.user.kobouser.surveys.all()]
            qs = qs.filter(answer__dataset_uuid_id__in=surveys)

        return qs


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

    list_filter = (AnswerLandscapeFilter, AnswerSurveyFilter, AnswerVillageFilter, )
    inlines = [AnswerGPSInline, AnswerGSInline, AnswerHHMembersInline, AnswerNRInline]
    resource_class = AnswerFromFileResource

    def get_queryset(self, request):
        # let's make sure that staff can only see their own data
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            surveys = [s.dataset_uuid for s in request.user.kobouser.surveys.all()]
            qs = qs.filter(dataset_uuid_id__in=surveys)

        return qs

@admin.register(Price)
class PriceAdmin(ImportExportModelAdmin):
    """
    Admin class for Connections
    """
    list_display = ['dataset_uuid', 'village', 'gs', 'price']
    list_filter = (PriceAnswerLandscapeFilter, AnswerSurveyFilter, PriceAnswerVillageFilter,)


@admin.register(District)
class DistrictAdmin(GeoModelAdmin):
    """
    Admin class for Districts
    """
    map_template = 'admin/shp_file_upload.html'
    list_display = ['district', 'landscape']

    def get_queryset(self, request):
        # let's make sure that staff can only see their own data
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            surveys = [s.dataset_uuid for s in request.user.kobouser.surveys.all()]
            landscapes = Answer.objects.filter(dataset_uuid_id__in=surveys).only('landscape').order_by(
                'landscape').distinct('landscape')
            landscape_names = list()

            for landscape in landscapes:
                landscape_names.append(landscape.landscape)
            qs = qs.filter(landscape__in=landscape_names)

        return qs


@admin.register(Landscape)
class LandscapeAdmin(GeoModelAdmin):
    """
    Admin class for Landscapes
    """
    map_template = 'admin/shp_file_upload.html'
    list_display = ['landscape']

    def get_queryset(self, request):
        # let's make sure that staff can only see their own data
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            surveys = [s.dataset_uuid for s in request.user.kobouser.surveys.all()]
            landscapes = Answer.objects.filter(dataset_uuid_id__in=surveys).only('landscape').order_by(
                'landscape').distinct('landscape')
            landscape_names = list()

            for landscape in landscapes:
                landscape_names.append(landscape.landscape)
            qs = qs.filter(landscape__in=landscape_names)

        return qs


@admin.register(BNSForm)
class BNSFormAdmin(ImportExportModelAdmin):
    """
    Admin class for BNS FormsConnections
    """
    list_display = ['dataset_name', 'dataset_year', 'dataset_owner', 'dataset_uuid',
                    'last_submission_time', 'last_update_time', 'last_checked_time', 'kobo_managed']

    def get_queryset(self, request):
        # let's make sure that staff can only see their own data
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            surveys = [s.dataset_uuid for s in request.user.kobouser.surveys.all()]
            qs = qs.filter(dataset_uuid__in=surveys)

        return qs

    def sync(self, request, queryset):
        """
        Add action to fetch latest data from Kobo
        :param request:
        :param queryset:
        :return:
        """

        for form in queryset:

            if form.kobo_managed == True:

                dataset = get_kobo_data(form.auth_user, form.dataset_id)
                dataset = normalize_data(dataset)

                now = datetime.now()

                a = sync_answers(dataset, form.dataset_uuid, now)
                if a["status"] == "success":
                    self.message_user(request,
                                      "Successfully updated {} answers for form {}".format(a["count"], form.dataset_name))

                    b = sync_answersgps(dataset, form.dataset_uuid, now)
                    if b["status"] == "success":
                        self.message_user(request,
                                          "Successfully updated {} GPS coordinates for form {}".format(b["count"],
                                                                                                       form.dataset_name))
                    else:
                        self.message_user(request,
                                          "Failed to updated GPS coordinates for form {}".format(form.dataset_name),
                                          level=messages.ERROR)

                    c = sync_answersgs(dataset, form.dataset_uuid, now)
                    if c["status"] == "success":
                        self.message_user(request, "Successfully updated {} Goods & Service entries for form {}".format(
                            c["count"],
                            form.dataset_name))
                    else:
                        self.message_user(request,
                                          "Failed to updated Goods & Service entries for form {}".format(form.dataset_name),
                                          level=messages.ERROR)

                    d = sync_answershhmembers(dataset, form.dataset_uuid, now)
                    if d["status"] == "success":
                        self.message_user(request, "Successfully updated {} household member entries for form {}".format(
                                              d["count"],
                                              form.dataset_name))
                    else:
                        self.message_user(request,
                                          "Failed to updated household member entries for form {}".format(form.dataset_name),
                                          level=messages.ERROR)

                    e = sync_answersnr(dataset, form.dataset_uuid, now)
                    if e["status"] == "success":
                        self.message_user(request,
                                          "Successfully updated {} natural resource entries for form {}".format(d["count"],
                                              form.dataset_name))
                    else:
                        self.message_user(request,
                                          "Failed to updated Natural Resources entries for form {}".format(form.dataset_name),
                                          level=messages.ERROR)

                    form.last_update_time = datetime.now()
                    form.save()

                else:
                    self.message_user(request, "Failed to updated answers for form {}".format(form.dataset_name),
                                      level=messages.ERROR)
            else:
                self.message_user(request, "Form {} is not managed in Kobo. No data synced".format(form.dataset_name),
                                  level=messages.WARNING)

    actions = [sync]
    sync.short_description = "Sync data"


@admin.register(BNSFormPrice)
class BNSFormPriceAdmin(ImportExportModelAdmin):
    """
    Admin class for BNS Price Forms
    """
    list_display = ['dataset_name', 'related_dataset', 'dataset_year', 'dataset_owner', 'dataset_uuid',
                    'last_submission_time', 'last_update_time', 'last_checked_time', 'kobo_managed']

    def get_queryset(self, request):
        # let's make sure that staff can only see their own data
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            surveys = [s.dataset_name for s in request.user.kobouser.surveys.all()]
            qs = qs.filter(related_dataset__in=surveys)

        return qs

    def sync(self, request, queryset):
        """
        Add action to fetch latest data from Kobo
        :param request:
        :param queryset:
        :return:
        """

        for form in queryset:

            if form.kobo_managed == True:

                dataset = get_kobo_data(form.auth_user, form.dataset_id)
                now = datetime.now()

                a = sync_price(dataset, form.related_uuid, now)

                if a["status"] == "success":
                    form.last_update_time = datetime.now()
                    form.save()
                    self.message_user(request, "Successfully updated {} prices for form {}".format(a["count"],
                                                                                               form.dataset_name))
                else:
                    self.message_user(request, "Failed to updated prices for form {}".format(form.dataset_name),
                                  level=messages.ERROR)

            else:
                self.message_user(request, "Form {} is not managed in Kobo. No data synced".format(form.dataset_name),
                                  level=messages.WARNING)

    actions = [sync]
    sync.short_description = "Sync data"
