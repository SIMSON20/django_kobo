from import_export import resources
from .models import AME, Answer, AnswerGPS, AnswerGS, AnswerHHMembers, AnswerNR
from import_export.fields import Field
from django.contrib.gis.geos import GEOSGeometry


class AnswerFromKoboResource(resources.ModelResource):

    form = None
    answer_id = Field(attribute='answer_id', column_name='_uuid')
    dataset_uuid = Field(attribute='dataset_uuid', column_name='dataset_uuid')
    landscape = Field(attribute='landscape', column_name='landscape')
    surveyor = Field(attribute='surveyor', column_name='surveyor')
    participant = Field(attribute='participant', column_name='participant')
    arrival = Field(attribute='arrival', column_name='arrival')
    district = Field(attribute='district', column_name='district')
    village = Field(attribute='village', column_name='village')
    hh_type_control = Field(attribute='hh_type_control', column_name='hh_type_control')
    hh_type_org_benef = Field(attribute='hh_type_org_benef', column_name='hh_type_org_benef')
    hh_type_other_benef = Field(attribute='hh_type_other_benef', column_name='hh_type_other_benef')
    hh_id = Field(attribute='hh_id', column_name='hh_id')
    livelihood_1 = Field(attribute='livelihood_1', column_name='livelihoods/l1')
    livelihood_2 = Field(attribute='livelihood_2', column_name='livelihoods/l2')
    livelihood_3 = Field(attribute='livelihood_3', column_name='livelihoods/l3')
    livelihood_4 = Field(attribute='livelihood_4', column_name='livelihoods/l4')
    benef_project = Field(attribute='benef_project', column_name='benef_project')
    explain_project = Field(attribute='explain_project', column_name='explain_project')
    know_pa = Field(attribute='know_pa', column_name='know_pa')
    benef_pa = Field(attribute='benef_pa', column_name='benef_pa')
    explain_benef_pa = Field(attribute='explain_benef_pa', column_name='explain_benef_PA')
    bns_plus = Field(attribute='bns_plus', column_name='bns_plus')
    survey_date = Field(attribute='survey_date', column_name='_submission_time')

    class Meta:
        model = Answer
        import_id_fields = ('answer_id',)

    def before_import_row(self, row, **kwargs):
        #import pdb; pdb.set_trace()
        row["dataset_uuid"] = self.form
        row["hh_type_control"] = None if row["hh_type"] is None else True if 'control' in row["hh_type"] else False
        row["hh_type_org_benef"] = None if row["hh_type"] is None else True if 'org_benef' in row["hh_type"] else False
        row["hh_type_other_benef"] = None if row["hh_type"] is None else True if 'other_benef' in row["hh_type"] else False
        row["hh_id"] = row["_uuid"] if (row["hh_id"] is None or row["hh_id"].upper() == "NEW") else row["hh_id"]
        row["benef_project"] = None if row["benef_project"] is None else True if row["benef_project"].lower() == 'yes' else False
        row["benef_pa"] = None if row["benef_PA"] is None else True if row["benef_PA"].lower() == 'yes' else False
        row["know_pa"] = None if row["know_PA"] is None else True if row["know_PA"].lower() == 'yes' else False


class AnswerGPSFromKoboResource(resources.ModelResource):
    answer_id = Field(attribute='answer_id', column_name='_uuid')
    lat = Field(attribute='lat', column_name='lat')
    long = Field(attribute='long', column_name='long')
    geom = Field(attribute='geom', column_name='geom')

    class Meta:
        model = AnswerGPS
        import_id_fields = ('answer_id',)

    def before_import_row(self, row, **kwargs):

        row["answer_id"] = Answer.objects.get(answer_id=row["_uuid"])
        row["lat"] = None if row["gps/lat"] is None and row["_geolocation"][0] is None else float(row["gps/lat"]) if row["_geolocation"][0] is None else row["_geolocation"][0]
        row["long"] = None if row["gps/long"] is None and row["_geolocation"][1] is None else float(row["gps/long"]) if row["_geolocation"][1] is None else row["_geolocation"][1]

        if not (row["lat"] is None or row["long"] is None) and -90 <= row["lat"] <= 90 and -180 <= row["long"] <= 180:
            row["geom"] = GEOSGeometry('POINT({} {})'.format(row["long"], row["lat"]), srid=4326)
        else:
            row["geom"] = None

"""
class AnswerGSFromKoboResource(resources.ModelResource):
    id =
    answer_id = Field(attribute='answer_id', column_name='_uuid')
    gs = models.TextField()
    necessary = models.NullBooleanField()
    have = models.NullBooleanField()
    quantity = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=1000, decimal_places=1000, blank=True, null=True)

    class Meta:
        model = AnswerGS
"""