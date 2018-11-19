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
    landscape = Field(attribute='landscape', column_name='landscape')
    surveyor = Field(attribute='surveyor', column_name='_submitted_by')
    gov_group = Field(attribute='gov_group', column_name='gov_group')
    objective = Field(attribute='objective', column_name='objective')
    women = Field(attribute='women', column_name='women')
    jurisdiction = Field(attribute='jurisdiction', column_name='jurisdiction')
    members = Field(attribute='members', column_name='members')
    survey_date = Field(attribute='survey_date', column_name='_submission_time')
    last_update = Field(attribute='last_update', column_name='last_update')

    class Meta:
        model = NRGTAnswer
        import_id_fields = ('answer_id',)

    def before_import_row(self, row, **kwargs):
        row["dataset_uuid"] = KoboData.objects.get(dataset_uuid=row["_xform_id_string"])

        row["landscape"] = row["group_info/landscape"] if "group_info/landscape" in row.keys() and \
                                                          not row["group_info/landscape"] == None else \
            row["landscape"] if "landscape" in row.keys() else \
                None

        row["gov_group"] = row["group_info/gov_group"] if "group_info/gov_group" in row.keys() and \
                                                          not row["group_info/gov_group"] == None else \
            row["gov_group"] if "gov_group" in row.keys() else \
                None

        row["objective"] = row["group_info/objective"] if "group_info/objective" in row.keys() and \
                                                          not row["group_info/objective"] == None else \
            row["objective"] if "objective" in row.keys() else \
                None

        row["women"] = row["group_info/women"] if "group_info/women" in row.keys()  and \
                                                         not row["group_info/women"] == None else\
            row["women"] if "women" in row.keys() else \
                None

        row["jurisdiction"] = row["group_info/jurisdiction"] if "group_info/jurisdiction" in row.keys() and \
                                                                not row["group_info/jurisdiction"] == None else \
            row["jurisdiction"] if "jurisdiction" in row.keys() else \
                None

        row["members"] = row["group_info/members"] if "group_info/members" in row.keys() and \
                                                      not row["group_info/members"] == None else \
            row["members"] if "members" in row.keys() else \
                None

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
