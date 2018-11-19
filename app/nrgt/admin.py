from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin
from .models import NRGTForm, NRGTAnswer, NRGTAnswerGS
from .resources import NRGTAnswerGSFromFileResource, NRGTAnswerFromFileResource, NRGTAnswerGSFromKoboResource, \
    NRGTAnswerFromKoboResource
import json
from datetime import datetime
import tablib
from kobo.utils import get_kobo_data, normalize_data


@admin.register(NRGTAnswerGS)
class NRGTAnswerGSAdmin(ImportExportModelAdmin):
    list_display = ['answer_id', 'code', 'survey_date', 'member', 'gender', 'motivation', 'instutional_framework',
    'fairness', 'enact_decision', 'knowledge_skills', 'participation', 'transparency', 'resources', 'diversity',
    'held_accountable', 'accountability', 'legitimacy']
    resource_class = NRGTAnswerGSFromFileResource


class NRGTAnswerGSInline(admin.StackedInline):
    model = NRGTAnswerGS
    extra = 1


@admin.register(NRGTAnswer)
class AnswerAdmin(ImportExportModelAdmin):
    """
    Admin class for Connections
    """
    list_display = ['answer_id', 'dataset_uuid', 'landscape', 'surveyor', 'gov_group', 'women',
                    'jurisdiction', 'members', 'survey_date', 'last_update']

    inlines = [NRGTAnswerGSInline]
    resource_class = NRGTAnswerFromFileResource


@admin.register(NRGTForm)
class NRGTFormAdmin(ImportExportModelAdmin):
    """
    Admin class for NRGT FormsConnections
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
            self._sync_nrgt(dataset, form, request)
            form.last_update_time = datetime.now()
            form.save()

    def _sync_nrgt(self, dataset, form, request):
        """
        Syncs selected BNS data with Kobo
        :param dataset:
        :param form:
        :param request:
        :return:
        """
        dataset = normalize_data(dataset)

        answer_resource = NRGTAnswerFromKoboResource()
        answer_gs_resource = NRGTAnswerGSFromKoboResource()

        answer_resource.form = form

        now = datetime.now()

        # Update main Answer table
        result = answer_resource.import_data(dataset, raise_errors=True, dry_run=True)
        if not result.has_errors():
            answer_resource.import_data(dataset, dry_run=False)

            # Delete not updated records
            NRGTAnswer.objects.filter(dataset_uuid=form.dataset_uuid).filter(last_update__lt=now).delete()

            self.message_user(request,
                              "Successfully updated {} answers for form {}".format(len(dataset), form.dataset_name))

            # Update NRGTAnswerGS table
            gs_dataset = self._extract_gs(dataset.dict)

            result = answer_gs_resource.import_data(gs_dataset, raise_errors=True, dry_run=True)
            if not result.has_errors():
                answer_gs_resource.import_data(gs_dataset, dry_run=False)

                # Delete not updated records
                NRGTAnswerGS.objects.filter(answer__dataset_uuid=form.dataset_uuid).filter(last_update__lt=now).delete()

                self.message_user(request,
                                  "Successfully updated {} Group Score entries for form {}".format(len(gs_dataset),
                                                                                                       form.dataset_name))
            else:
                self.message_user(request,
                                  "Failed to updated Group Score entries for form {}".format(form.dataset_name),
                                  level=messages.ERROR)

        else:
            self.message_user(request, "Failed to updated answers for form {}".format(form.dataset_name),
                              level=messages.ERROR)
            # raise forms.ValidationError("Import of Answers failed!")


    @staticmethod
    def _extract_gs(dataset):
        """
        Read Kobo data and extract Group Score from answers
        Convert table and write each Group Score in a seperate row
        :param dataset:
        :return:
        """

        new_dataset = list()

        for data_row in dataset:

            answer_id = data_row["_uuid"]


            if data_row["group_scores"] is not None:
                for group in data_row["group_scores"]:

                    row = dict()
                    row["answer_id"] = answer_id
                    row["code"] = group["group_scores/code"] if "group_scores/code" in group.keys() else \
                        group["group_scores/group_header/code"] if "group_scores/group_header/code" in group.keys() else \
                            None

                    row["survey_date"] = group["group_scores/survey_date"] if "group_scores/survey_date" in group.keys() else \
                        group["group_scores/group_header/survey_date"] if "group_scores/group_header/survey_date" in group.keys() else \
                            None

                    row["survey_date"] = group["group_scores/survey_date"] if "group_scores/survey_date" in group.keys() else \
                        group["group_scores/group_header/survey_date"] if "group_scores/group_header/survey_date" in group.keys() else \
                            None

                    row["_member"] = group["group_scores/member"] if "group_scores/member" in group.keys() else \
                        group["group_scores/group_header2/member"] if "group_scores/group_header2/member" in group.keys() else \
                            None

                    row["member"] = None if row["_member"] is None else True if row["_member"].lower() == 'yes' else False

                    row["gender"] = group["group_scores/gender"] if "group_scores/gender" in group.keys() else \
                        group["group_scores/group_header2/gender"] if "group_scores/group_header2/gender" in group.keys() else \
                            None

                    row["motivation"] = group["group_scores/motivation"] if "group_scores/motivation" in group.keys() else \
                        group["group_scores/group_capacity/motivation"] if "group_scores/group_capacity/motivation" in group.keys() else \
                            None

                    row["institutional_framework"] = group["group_scores/institutional_framework"] if "group_scores/institutional_framework" in group.keys() else \
                        group["group_scores/group_capacity/institutional_framework"] if "group_scores/group_capacity/institutional_framework" in group.keys() else \
                            None

                    row["fairness"] = group["group_scores/fairness"] if "group_scores/fairness" in group.keys() else \
                        group["group_scores/group_authority/fairness"] if "group_scores/group_authority/fairness" in group.keys() else \
                            None

                    row["enact_decision"] = group["group_scores/enact_decision"] if "group_scores/enact_decision" in group.keys() else \
                        group["group_scores/group_power/enact_decision"] if "group_scores/group_power/enact_decision" in group.keys() else \
                            None

                    row["knowledge_skills"] = group["group_scores/knowledge_skills"] if "group_scores/knowledge_skills" in group.keys() else \
                        group["group_scores/group_capacity/knowledge_skills"] if "group_scores/group_capacity/knowledge_skills" in group.keys() else \
                            None

                    row["participation"] = group["group_scores/participation"] if "group_scores/participation" in group.keys() else \
                        group["group_scores/group_authority/participation"] if "group_scores/group_authority/participation" in group.keys() else \
                            None

                    row["transparency"] = group["group_scores/transparency"] if "group_scores/transparency" in group.keys() else \
                        group["group_scores/group_authority/transparency"] if "group_scores/group_authority/transparency" in group.keys() else \
                            None

                    row["resources"] = group["group_scores/resources"] if "group_scores/resources" in group.keys() else \
                        group["group_scores/group_capacity/resources"] if "group_scores/group_capacity/resources" in group.keys() else \
                            None

                    row["diversity"] = group["group_scores/diversity"] if "group_scores/diversity" in group.keys() else \
                            None

                    row["held_accountable"] = group["group_scores/held_accountable"] if "group_scores/held_accountable" in group.keys() else \
                        group["group_scores/group_power/held_accountable"] if "group_scores/group_power/held_accountable" in group.keys() else \
                            None

                    row["accountability"] = group["group_scores/accountability"] if "group_scores/accountability" in group.keys() else \
                        group["group_scores/group_authority/accountability"] if "group_scores/group_authority/accountability" in group.keys() else \
                            None

                    row["legitimacy"] = group["group_scores/legitimacy"] if "group_scores/legitimacy" in group.keys() else \
                        group["group_scores/group_authority/legitimacy"] if "group_scores/group_authority/legitimacy" in group.keys() else \
                            None


                    new_dataset.append(row)

        return tablib.Dataset().load(json.dumps(new_dataset, sort_keys=True))

    actions = [sync]
    sync.short_description = "Sync data"
