from django.contrib.gis.db import models
from kobo.models import Connection, KoboData
import uuid
from datetime import datetime


class NRGTAnswer(models.Model):
    answer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset_uuid = models.ForeignKey(KoboData, on_delete=models.CASCADE)
    landscape = models.TextField(blank=True, null=True)
    surveyor = models.TextField(blank=True, null=True)
    survey_date = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField(default=datetime.now, editable=False)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'