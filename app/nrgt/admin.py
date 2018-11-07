from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import NRGTForm, NRGTAnswer, NRGTAnswerGS


@admin.register(NRGTAnswerGS)
class AnswerNRAdmin(ImportExportModelAdmin):
    list_display = ['answer_id', 'code', 'survey_date', 'member', 'gender', 'motivation', 'instutional_framework',
    'fairness', 'enact_decision', 'knowledge_skills', 'participation', 'transparency', 'resources', 'diversity',
    'held_accountable', 'accountability', 'legitimacy']
    #resource_class = NRGTAnswerGSFromFileResource


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
    #resource_class = NRGTAnswerFromFileResource


@admin.register(NRGTForm)
class NRGTFormAdmin(ImportExportModelAdmin):
    """
    Admin class for NRGT FormsConnections
    """
    list_display = ['dataset_name', 'dataset_year', 'dataset_owner', 'dataset_uuid',
                    'last_submission_time', 'last_update_time', 'last_checked_time', 'kobo_managed']



