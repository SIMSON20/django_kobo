from import_export import resources
from .models import NRGTAnswer, NRGTAnswerGS
from kobo.models import KoboData
from import_export.fields import Field
from datetime import datetime


class NRGTAnswerFromFileResource(resources.ModelResource):
    class Meta:
        model = NRGTAnswer
        import_id_fields = ('answer_id',)


class NRGTAnswerGSFromFileResource(resources.ModelResource):
    class Meta:
        model = NRGTAnswerGS
        import_id_fields = ('answer_id', 'code',)


class NRGTAnswerFromKoboResource(resources.ModelResource):

    answer_id = Field(attribute='answer_id', column_name='_uuid')
    dataset_uuid = Field(attribute='dataset_uuid', column_name='dataset_uuid')
    landscape = Field(attribute='landscape', column_name='group_info/landscape')
    surveyor = Field(attribute='surveyor', column_name='surveyor')
    gov_group = Field(attribute='gov_group', column_name='group_info/gov_group')
    objective = Field(attribute='objective', column_name='group_info/objective')
    women = Field(attribute='women', column_name='group_info/women')
    jurisdiction = Field(attribute='jurisdiction', column_name='group_info/jurisdiction')
    members = Field(attribute='members', column_name='group_info/members')
    survey_date = Field(attribute='survey_date', column_name='_submission_time')
    last_update = Field(attribute='last_update', column_name='last_update')

    class Meta:
        model = NRGTAnswer
        import_id_fields = ('answer_id',)

    def before_import_row(self, row, **kwargs):
        row["dataset_uuid"] = KoboData.objects.get(dataset_uuid=row["_xform_id_string"])
        row["last_update"] = datetime.now()


class NRGTAnswerGSFromKoboResource(resources.ModelResource):

    answer_id = Field(attribute='answer_id', column_name='answer_id')
    code = Field(attribute='code', column_name='code')
    survey_date = Field(attribute='survey_date ', column_name='survey_date')
    member = Field(attribute='member', column_name='member')
    gender = Field(attribute='gender', column_name='gender')
    motivation = Field(attribute='motivation', column_name='motivation')
    instutional_framework = Field(attribute='instutional_framework', column_name='institutional_framework')
    fairness = Field(attribute='fairness', column_name='fairness')
    enact_decision = Field(attribute='enact_decision', column_name='enact_decision')
    knowledge_skills = Field(attribute='knowledge_skills', column_name='knowledge_skills')
    participation = Field(attribute='participation', column_name='participation')
    transparency = Field(attribute='transparency', column_name='transparency')
    resources = Field(attribute='resources', column_name='resources')
    diversity = Field(attribute='diversity', column_name='diversity')
    held_accountable = Field(attribute='held_accountable', column_name='held_accountable')
    accountability = Field(attribute='accountability', column_name='accountability')
    legitimacy = Field(attribute='legitimacy', column_name='legitimacy')
    last_update = Field(attribute='last_update', column_name='last_update')

    class Meta:
        model = NRGTAnswerGS
        import_id_fields = ('answer_id', 'code',)

    def before_import_row(self, row, **kwargs):
        row["last_update"] = datetime.now()
