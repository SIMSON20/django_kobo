from django.contrib.gis.db import models
from kobo.models import KoboData
import uuid
from datetime import datetime


class AME(models.Model):
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=255)
    ame = models.FloatField(blank=True, null=True)
    calories = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = (('age', 'gender'),)
        verbose_name = 'AME'
        verbose_name_plural = 'AME'


class Answer(models.Model):
    answer_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    dataset_uuid = models.ForeignKey(KoboData, on_delete=models.CASCADE)
    landscape = models.CharField(max_length=255, blank=True, null=True)
    surveyor = models.CharField(max_length=255, blank=True, null=True)
    participant = models.CharField(max_length=255, blank=True, null=True)
    arrival = models.IntegerField(blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    village = models.CharField(max_length=255, blank=True, null=True)
    hh_type_control = models.NullBooleanField()
    hh_type_org_benef = models.NullBooleanField()
    hh_type_other_benef = models.NullBooleanField()
    hh_id = models.CharField(max_length=255, blank=True, null=True)
    livelihood_1 = models.CharField(max_length=255, blank=True, null=True)
    livelihood_2 = models.CharField(max_length=255, blank=True, null=True)
    livelihood_3 = models.CharField(max_length=255, blank=True, null=True)
    livelihood_4 = models.CharField(max_length=255, blank=True, null=True)
    benef_project = models.NullBooleanField()
    explain_project = models.CharField(max_length=255, blank=True, null=True)
    know_pa = models.NullBooleanField()
    benef_pa = models.NullBooleanField()
    explain_benef_pa = models.CharField(max_length=255, blank=True, null=True)
    bns_plus = models.CharField(max_length=255, blank=True, null=True)
    survey_date = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField(default=datetime.now(), editable=False)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'


class AnswerGPS(models.Model):
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE, )
    lat = models.DecimalField(max_digits=29, decimal_places=6, blank=True, null=True)
    long = models.DecimalField(max_digits=29, decimal_places=6, blank=True, null=True)
    geom = models.PointField(null=True)
    last_update = models.DateTimeField(default=datetime.now(), editable=False)

    class Meta:
        verbose_name = 'GPS'
        verbose_name_plural = 'GPS'


class AnswerGS(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE,  )
    gs = models.TextField()
    necessary = models.NullBooleanField()
    have = models.NullBooleanField()
    quantity = models.IntegerField(blank=True, null=True)
    last_update = models.DateTimeField(default=datetime.now(), editable=False)

    class Meta:
        unique_together = (('answer', 'gs'),)
        verbose_name = 'Good or Service'
        verbose_name_plural = 'Goods and Services'


class AnswerHHMembers(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE,)
    gender = models.TextField(blank=True, null=True)
    birth = models.IntegerField(blank=True, null=True)
    ethnicity = models.TextField(blank=True, null=True)
    head = models.NullBooleanField()
    last_update = models.DateTimeField(default=datetime.now(), editable=False)

    class Meta:
        verbose_name = 'HH Members'
        verbose_name_plural = 'HH Members'


class AnswerNR(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE,)
    nr = models.TextField()
    nr_collect = models.IntegerField(blank=True, null=True)
    last_update = models.DateTimeField(default=datetime.now(), editable=False)

    class Meta:
        verbose_name = 'Natural Resource'
        verbose_name_plural = 'Natural Resources'


class Price(models.Model):
    dataset_uuid = models.ForeignKey(KoboData, on_delete=models.CASCADE)
    village = models.TextField()
    surveyor = models.TextField(blank=True, null=True)
    gs = models.TextField()
    price = models.IntegerField(blank=True, null=True)
    last_update = models.DateTimeField(default=datetime.now(), editable=False)

    class Meta:
        unique_together = (('dataset_uuid', 'village', 'gs'),)
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'