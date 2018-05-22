from import_export import resources
from .models import AME, Answer, AnswerGPS, AnswerGS, AnswerHHMembers, AnswerNR
from import_export.fields import Field
from django.contrib.gis.geos import GEOSGeometry


class AnswerFromKoboResource(resources.ModelResource):

    answer_id = Field(attribute='answer_id', column_name='_uuid')
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
    know_pa = Field(attribute='know_pa', column_name='know_PA')
    benef_pa = Field(attribute='benef_pa', column_name='benef_PA')
    explain_benef_pa = Field(attribute='explain_benef_pa', column_name='explain_benef_PA')
    bns_plus = Field(attribute='bns_plus', column_name='bns_plus')
    survey_date = Field(attribute='survey_date', column_name='_submission_time')

    class Meta:
        model = Answer
        import_id_fields = ('answer_id',)

    def before_import_row(self, row, **kwargs):
        row["hh_type_control"] = True if 'control' in row["hh_type"] else False
        row["hh_type_org_benef"] = True if 'org_benef' in row["hh_type"] else False
        row["hh_type_other_benef"] = True if 'other_benef' in row["hh_type"] else False
        row["hh_id"] = row["_uuid"] if (row["hh_id"] is None or row["hh_id"].upper() == "NEW") else row["hh_id"]


class AnswerGPSFromKoboResource(resources.ModelResource):
    answer_id = Field(attribute='answer_id', column_name='_uuid')
    lat = Field(attribute='lat', column_name='lat')
    long = Field(attribute='long', column_name='long')
    geom = Field(attribute='geom', column_name='geom')

    class Meta:
        model = AnswerGPS
        import_id_fields = ('answer_id',)

    def before_import_row(self, row, **kwargs):

        row["lat"] = row["gps/lat"] if row["_geolocation"][0] is None else row["_geolocation"][0]
        row["long"] = row["gps/long"] if row["_geolocation"][1] is None else row["_geolocation"][1]
        if -90 <= row["lat"] <= 90 and -180 <= row["long"] <= 180:
            row["geom"] = GEOSGeometry('POINT({} {}, srid=4326)'.format(row["long"], row["lat"]))
        else:
            row["geom"] = None
