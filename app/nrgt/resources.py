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
        row["last_update"] = datetime.now()


class NRGTAnswerGSFromKoboResource(resources.ModelResource):

    answer_id = Field(attribute='answer_id', column_name='_uuid')
    code = Field(attribute='code', column_name='group_scores/code')
    survey_date = Field(attribute='survey_date ', column_name='group_scores/survey_date')
    member = Field(attribute='member', column_name='member')
    gender = Field(attribute='gender', column_name='group_scores/gender')
    motivation = Field(attribute='motivation', column_name='group_scores/motivation')
    instutional_framework = Field(attribute='instutional_framework', column_name='group_scores/institutional_framework')
    fairness = Field(attribute='fairness', column_name='group_scores/fairness')
    enact_decision = Field(attribute='enact_decision', column_name='group_scores/enact_decision')
    knowledge_skills = Field(attribute='knowledge_skills', column_name='group_scores/knowledge_skills')
    participation = Field(attribute='participation', column_name='group_scores/participation')
    transparency = Field(attribute='transparency', column_name='group_scores/transparency')
    resources = Field(attribute='resources', column_name='group_scores/resources')
    diversity = Field(attribute='diversity', column_name='group_scores/diversity')
    held_accountable = Field(attribute='held_accountable', column_name='group_scores/held_accountable')
    accountability = Field(attribute='accountability', column_name='group_scores/accountability')
    legitimacy = Field(attribute='legitimacy', column_name='group_scores/legitimacy')
    last_update = Field(attribute='last_update', column_name='last_update')

    class Meta:
        model = NRGTAnswerGS
        import_id_fields = ('answer_id', 'code',)

    def before_import_row(self, row, **kwargs):
        row["member"] = None if row["group_scores/member"] is None else True if row["group_scores/member"].lower() == 'yes' else False
        row["last_update"] = datetime.now()
