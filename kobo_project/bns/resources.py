from import_export import resources
from .models import AME, Answer, AnswerGPS, AnswerGS, AnswerHHMembers, AnswerNR, Price
from kobo.models import KoboData
from import_export.fields import Field
from django.contrib.gis.geos import GEOSGeometry
from datetime import datetime


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
    last_update = Field(attribute='last_update', column_name='last_update')

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
        row["last_update"] = datetime.now()


class AnswerGPSFromKoboResource(resources.ModelResource):
    answer_id = Field(attribute='answer_id', column_name='_uuid')
    lat = Field(attribute='lat', column_name='lat')
    long = Field(attribute='long', column_name='long')
    geom = Field(attribute='geom', column_name='geom')
    last_update = Field(attribute='last_update', column_name='last_update')

    class Meta:
        model = AnswerGPS
        import_id_fields = ('answer_id',)

    def before_import_row(self, row, **kwargs):

        row["answer_id"] = Answer.objects.get(answer_id=row["_uuid"])

        if row["_geolocation"][0] is not None:
            row["lat"] = row["_geolocation"][0]
        elif row["gps/lat"] is not None:
            row["lat"] = float(row["gps/lat"])
        else:
            row["lat"] = None

        if row["_geolocation"][1] is not None:
            row["long"] = row["_geolocation"][1]
        elif row["gps/long"] is not None:
            row["long"] = float(row["gps/long"])
        else:
            row["long"] = None

        if not (row["lat"] is None or row["long"] is None) and -90 <= row["lat"] <= 90 and -180 <= row["long"] <= 180:
            row["geom"] = GEOSGeometry('POINT({} {})'.format(row["long"], row["lat"]), srid=4326)
        else:
            row["geom"] = None

        row["last_update"] = datetime.now()


class AnswerGSFromKoboResource(resources.ModelResource):
    # id =
    answer_id = Field(attribute='answer_id', column_name='answer_id')
    gs = Field(attribute='gs', column_name='gs')
    have = Field(attribute='have', column_name='have')
    necessary =Field(attribute='necessary', column_name='necessary')
    quantity = Field(attribute='quantity', column_name='quantity')
    last_update = Field(attribute='last_update', column_name='last_update')

    class Meta:
        model = AnswerGS
        import_id_fields = ('answer_id', 'gs', )

    def before_import_row(self, row, **kwargs):
        row["last_update"] = datetime.now()
        # row["answer_id"] = Answer.objects.get(answer_id=row["answer_id"])


class AnswerHHMembersFromKoboResource(resources.ModelResource):

    answer_id = Field(attribute='answer_id', column_name='answer_id')
    gender = Field(attribute='gender', column_name='gender')
    birth = Field(attribute='birth', column_name='birth')
    ethnicity = Field(attribute='ethnicity', column_name='ethnicity')
    head = Field(attribute='head', column_name='head')
    last_update = Field(attribute='last_update', column_name='last_update')

    class Meta:
        model = AnswerHHMembers
        import_id_fields = ('answer_id', 'gender', 'birth', ) # might cause issues with HH members of same age and gender, not sure how often this actually happens

    def before_import_row(self, row, **kwargs):
        row["last_update"] = datetime.now()
        # row["answer_id"] = Answer.objects.get(answer_id=row["answer_id"])


class AnswerNRFromKoboResource(resources.ModelResource):
    answer_id = Field(attribute='answer_id', column_name='answer_id')
    nr = Field(attribute='nr', column_name='nr')
    nr_collect = Field(attribute='nr_collect', column_name='nr_collect')
    last_update = Field(attribute='last_update', column_name='last_update')

    class Meta:
        model = AnswerNR
        import_id_fields = ('answer_id', 'nr', )

    def before_import_row(self, row, **kwargs):
        row["last_update"] = datetime.now()


class PriceFromKoboResource(resources.ModelResource):
    dataset_uuid = Field(attribute='dataset_uuid', column_name='dataset_uuid')
    gs = Field(attribute='gs', column_name='gs')
    have = Field(attribute='have', column_name='have')
    necessary =Field(attribute='necessary', column_name='necessary')
    quantity = Field(attribute='quantity', column_name='quantity')
    last_update = Field(attribute='last_update', column_name='last_update')

    class Meta:
        model = Price
        import_id_fields = ('dataset_uuid', 'gs', )

    def before_import_row(self, row, **kwargs):
        row["dataset_uuid"] = KoboData.objects.get(dataset_uuid=row["dataset_uuid"])
        row["last_update"] = datetime.now()