from django.shortcuts import render
from .models import Answer, Landscape
from kobo.models import KoboData, KoboUser
from django_tables2 import RequestConfig
from django.apps import apps
import django_tables2 as tables
from django_tables2.export.export import TableExport
from django.db.models import Count
from django.db.models import Q
import django_filters
from .decorators import has_landscape_access, has_survey_access
# from django.contrib.auth.decorators import login_required, user_passes_test


def _landscape_boundary(landscape_name):
    landscape_boundaries = Landscape.objects.raw("""SELECT 
                                                        id, 
                                                        landscape,  
                                                        ST_AsGeoJSON(geom) as geojson 
                                                    FROM bns_landscape 
                                                    WHERE landscape = '{}' LIMIT 1""".format(landscape_name))

    landscape_geojson = '{"type" : "FeatureCollection", "features" :['
    if len(landscape_boundaries):
        landscape_geojson += '{"type": "Feature", "properties": {"landscape": "%s"}, "geometry": %s }' % \
                             (landscape_name, landscape_boundaries[0].geojson)
    landscape_geojson += ']}'

    return landscape_geojson


def _landscape_villages(landscape_name):
    landscape_villages = Answer.objects.raw("""SELECT row_number() OVER () as answer_id,
                                                dataset_name, 
                                                village, 
                                                ST_AsGeoJSON(ST_SetSRID(ST_MakePoint(avg(long), avg(lat)),4326)) as geojson 
                                            FROM bns_answer a 
                                                JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid 
                                                JOIN bns_answergps g ON a.answer_id = g.answer_id
                                            WHERE landscape = '{}' AND lat != 0 AND long != 0
                                            GROUP BY dataset_name, village""".format(landscape_name))

    village_geojson = '{"type" : "FeatureCollection", "features" :['
    if len(landscape_villages):

        i = 0
        for village in landscape_villages:
            if i > 0:
                village_geojson += ','
            village_geojson += '{"type": "Feature", "properties": {"landscape": "%s", "survey": "%s", "village": "%s"}, "geometry": %s }' % \
                               (landscape_name, village.dataset_name, village.village, village.geojson)
            i += 1
    village_geojson += ']}'

    return village_geojson


def _survey_villages(survey):
    survey_villages = Answer.objects.raw("""SELECT row_number() OVER () as answer_id,
                                                dataset_name, 
                                                village, 
                                                ST_AsGeoJSON(ST_SetSRID(ST_MakePoint(avg(long), avg(lat)),4326)) as geojson 
                                            FROM bns_answer a 
                                                JOIN kobo_kobodata k ON a.dataset_uuid_id = k.dataset_uuid 
                                                JOIN bns_answergps g ON a.answer_id = g.answer_id
                                            WHERE dataset_name = '{}' AND lat != 0 AND long != 0
                                            GROUP BY dataset_name, village""".format(survey))

    village_geojson = '{"type" : "FeatureCollection", "features" :['
    if len(survey_villages):
        i = 0
        for village in survey_villages:
            if i > 0:
                village_geojson += ','
            village_geojson += '{"type": "Feature", "properties": {"survey": "%s", "village": "%s"}, "geometry": %s }' % \
                               (village.dataset_name, village.village, village.geojson)
            i += 1
    village_geojson += ']}'

    return village_geojson


def index(request):
    return render(request, 'bns_home.html')
    #return HttpResponse("Hello, world. You're at the bns index.")



#@login_required
def surveys(request):
    surveys = KoboData.objects.annotate(num_answers=Count('answer')).filter(num_answers__gte=1)
    #if not request.user.is_superuser:
    #    user_surveys = KoboUser.objects.filter(user=request.user)
    #    surveys = surveys.filter(kobouser__in=user_surveys)
    return render(request, 'bns_surveys.html', {'surveys': surveys})


#@login_required
def survey(request, survey_name):
    survey = KoboData.objects.filter(dataset_name=survey_name)
    village_geojson = _survey_villages(survey_name)

    # TODO review return values,  can be better structured
    return render(request, 'bns_survey.html', {'survey': survey,
                                               'surveys': [survey],
                                               'landscape_geojson': '{"type" : "FeatureCollection", "features" :[]}',
                                               'village_geojson': village_geojson,
                                               'survey_name': survey_name})


#@login_required
@has_survey_access
def survey_query(request, survey_name, query_name):
    # username = None
    mymodel = apps.get_model('bns', query_name)

    class myTable(tables.Table):
        name = mymodel.table_name

        class Meta:
            model = mymodel
            template_name = 'bootstrap.html'

    class myFilter(django_filters.FilterSet):
        class Meta:
            model = mymodel
            fields = mymodel.filter_fields

    queryset = mymodel.objects.filter(dataset_uuid__dataset_name=survey_name)

    filter = myFilter(request.GET, queryset=queryset)

    table = myTable(filter.qs)
    RequestConfig(request).configure(table)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('{}.{}'.format(mymodel.table_name, export_format))

    table.paginate(page=request.GET.get('page', 1), per_page=request.GET.get('per_page', 10))
    table.export_formats = ['csv', 'xls', 'json', 'tsv']

    return render(request, 'bns_survey_query.html', {'table': table, 'filter': filter, 'survey_name': survey_name})


#@login_required
def landscapes(request):
    landscapes = Answer.objects.values("landscape").annotate(num_answers=Count('answer_id')).filter(num_answers__gte=1).filter(~Q(landscape=None))
    return render(request, 'bns_landscapes.html', {'landscapes': landscapes})


#@login_required
def landscape(request, landscape_name):

    surveys = KoboData.objects.annotate(num_answers=Count('answer')).filter(answer__landscape=landscape_name).filter(num_answers__gte=1)
    landscape_geojson = _landscape_boundary(landscape_name)
    village_geojson = _landscape_villages(landscape_name)

    return render(request, 'bns_landscape.html', {'surveys': surveys,
                                                  'landscape_geojson': landscape_geojson,
                                                  'village_geojson': village_geojson,
                                                  'landscape_name': landscape_name})


#@login_required
@has_landscape_access
def landscape_query(request, landscape_name, query_name, surveys=[]):
    # username = None
    mymodel = apps.get_model('bns', query_name)

    class myTable(tables.Table):
        name = mymodel.table_name

        class Meta:
            model = mymodel
            template_name = 'bootstrap.html'

    class myFilter(django_filters.FilterSet):
        class Meta:
            model = mymodel
            fields = mymodel.filter_fields

    queryset = mymodel.objects.filter(landscape=landscape_name)

    if not request.user.is_superuser:
        if not 'landscape' in query_name.lower():
            queryset = queryset.filter(dataset_uuid_id__in=surveys)

    filter = myFilter(request.GET, queryset=queryset)

    table = myTable(filter.qs)
    RequestConfig(request).configure(table)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('{}.{}'.format(mymodel.table_name, export_format))

    table.paginate(page=request.GET.get('page', 1), per_page=request.GET.get('per_page', 10))
    table.export_formats = ['csv', 'xls', 'json', 'tsv']

    return render(request, 'bns_landscape_query.html', {'table': table, 'filter': filter, 'landscape_name': landscape_name})
