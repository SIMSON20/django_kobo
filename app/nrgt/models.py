from django.contrib.gis.db import models
from kobo.models import Connection, KoboData
import uuid
from datetime import datetime


class NRGTAnswer(models.Model):
    answer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset_uuid = models.ForeignKey(KoboData, on_delete=models.CASCADE)
    landscape = models.TextField(blank=True, null=True)
    surveyor = models.TextField(blank=True, null=True)
    gov_group = models.TextField(blank=True, null=True)
    objective = models.TextField(blank=True, null=True)
    women = models.FloatField(blank=True, null=True)
    jurisdiction = models.TextField(blank=True, null=True)
    members = models.IntegerField(blank=True, null=True)
    survey_date = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField(default=datetime.now, editable=False)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class NRGTAnswerGS(models.Model):
    answer = models.ForeignKey(NRGTAnswer, on_delete=models.CASCADE)
    code = models.TextField(blank=True, null=True)
    survey_date = models.DateTimeField(blank=True, null=True)
    member = models.NullBooleanField()
    gender = models.TextField(blank=True, null=True)
    motivation = models.IntegerField(blank=True, null=True)
    instutional_framework = models.IntegerField(blank=True, null=True)
    fairness = models.IntegerField(blank=True, null=True)
    enact_decision = models.IntegerField(blank=True, null=True)
    knowledge_skills = models.IntegerField(blank=True, null=True)
    participation = models.IntegerField(blank=True, null=True)
    transparency = models.IntegerField(blank=True, null=True)
    resources = models.IntegerField(blank=True, null=True)
    diversity = models.IntegerField(blank=True, null=True)
    held_accountable = models.IntegerField(blank=True, null=True)
    accountability = models.IntegerField(blank=True, null=True)
    legitimacy = models.IntegerField(blank=True, null=True)
    last_update = models.DateTimeField(default=datetime.now, editable=False)

    class Meta:
        verbose_name = 'Answer Governance Score'
        verbose_name_plural = 'Answers Governance Score'

    def __str__(self):
        return "{} ({})".format(self.answer_id, self.code)


class NRGTGroupScores(models.Model):
    answer = models.ForeignKey(NRGTAnswer, on_delete=models.CASCADE)
    landscape = models.TextField(blank=True, null=True)
    gov_group = models.TextField(blank=True, null=True)
    dataset_year = models.IntegerField(blank=True, null=True)
    legitimacy = models.FloatField(blank=True, null=True)
    accountability = models.FloatField(blank=True, null=True)
    transparency = models.FloatField(blank=True, null=True)
    participation = models.FloatField(blank=True, null=True)
    instutional_framework = models.FloatField(blank=True, null=True)
    fairness = models.FloatField(blank=True, null=True)
    motivation = models.FloatField(blank=True, null=True)
    knowledge_skills = models.FloatField(blank=True, null=True)
    resources = models.FloatField(blank=True, null=True)
    held_accountable = models.FloatField(blank=True, null=True)
    enact_decision = models.FloatField(blank=True, null=True)
    diversity = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'NRGT Group Score'
        verbose_name_plural = 'NRGT Group Scores'
        managed = False
        db_table = 'nrgt_group_scores'


class NRGTGroupAttributes(models.Model):
    answer = models.ForeignKey(NRGTAnswer, on_delete=models.CASCADE)
    landscape = models.TextField(blank=True, null=True)
    gov_group = models.TextField(blank=True, null=True)
    dataset_year = models.IntegerField(blank=True, null=True)
    autority = models.FloatField(blank=True, null=True)
    capacity = models.FloatField(blank=True, null=True)
    power = models.FloatField(blank=True, null=True)
    diversity = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = 'NRGT Group Attribute'
        verbose_name_plural = 'NRGT Group Attributes'
        managed = False
        db_table = 'nrgt_group_attributes'


class NRGTForm(models.Model):
    dataset_id = models.BigIntegerField(primary_key=True)
    auth_user = models.ForeignKey(Connection, on_delete=models.DO_NOTHING)
    dataset_name = models.TextField(blank=True, null=True)
    dataset_year = models.TextField(blank=True, null=True)
    dataset_owner = models.TextField(blank=True, null=True)
    dataset_uuid = models.TextField(blank=True, null=True)
    last_submission_time = models.DateTimeField(default=datetime.now, editable=False)
    last_update_time = models.DateTimeField(default=datetime.now, editable=False)
    last_checked_time = models.DateTimeField(default=datetime.now, editable=False)
    kobo_managed = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'NRGT Form'
        verbose_name_plural = 'NRGT Forms'
        managed = False
        db_table = 'nrgt_form'
