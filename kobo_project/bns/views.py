from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .models import AMEPerHH
from kobo.models import KoboData
from django_tables2 import RequestConfig
from django.apps import apps
import django_tables2 as tables
from django_tables2.export.export import TableExport
from django.db.models import Count

# Create your views here.


def index(request):
    return render(request, 'bns_home.html')
    #return HttpResponse("Hello, world. You're at the bns index.")


def surveys(request):
    surveys = KoboData.objects.annotate(num_answers=Count('answer')).filter(num_answers__gte=1)
    return render(request, 'surveys.html', {'surveys': surveys})


def survey(request, survey_name):
    survey = KoboData.objects.filter(dataset_name=survey_name)
    return render(request, 'survey.html', {'survey': survey, 'survey_name': survey_name})


def query(request, survey_name, query_name):
    # username = None
    mymodel = apps.get_model('bns', query_name)

    class myTable(tables.Table):
        name = mymodel.table_name

        class Meta:
            model = mymodel
            template_name = 'django_tables2/bootstrap.html'

    if request.user.is_authenticated:
        #if request.user.is_superuser:
        #    queryset = mymodel.objects.all()
        #else:
            # username = request.user.username
        queryset = mymodel.objects.filter(dataset_uuid__dataset_name=survey_name)
    else:
        pass #TODO: add handler for non authenticated users

    table = myTable(queryset)
    RequestConfig(request).configure(table)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('{}.{}'.format(mymodel.table_name, export_format))

    table.paginate(page=request.GET.get('page', 1), per_page=request.GET.get('per_page', 10))

    return render(request, 'query.html', {'table': table, 'survey_name': survey_name})
