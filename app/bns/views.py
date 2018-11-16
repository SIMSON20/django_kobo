from django.shortcuts import render
from .models import Answer
from kobo.models import KoboData
from django_tables2 import RequestConfig
from django.apps import apps
import django_tables2 as tables
from django_tables2.export.export import TableExport
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import django_filters

# Create your views here.


def index(request):
    return render(request, 'bns_home.html')
    #return HttpResponse("Hello, world. You're at the bns index.")



@login_required
def surveys(request):
    surveys = KoboData.objects.annotate(num_answers=Count('answer')).filter(num_answers__gte=1)
    return render(request, 'bns_surveys.html', {'surveys': surveys})


@login_required
def survey(request, survey_name):
    survey = KoboData.objects.filter(dataset_name=survey_name)
    return render(request, 'bns_survey.html', {'survey': survey, 'survey_name': survey_name})


@login_required
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


@login_required
def landscapes(request):
    landscapes = Answer.objects.values("landscape").annotate(num_answers=Count('answer_id')).filter(num_answers__gte=1).filter(~Q(landscape=None))
    return render(request, 'bns_landscapes.html', {'landscapes': landscapes})


@login_required
def landscape(request, landscape_name):
    surveys = KoboData.objects.annotate(num_answers=Count('answer')).filter(answer__landscape=landscape_name).filter(num_answers__gte=1)
    return render(request, 'bns_landscape.html', {'surveys': surveys, 'landscape_name': landscape_name})


@login_required
def landscape_query(request, landscape_name, query_name):
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

    filter = myFilter(request.GET, queryset=queryset)

    #for field in filter.form.fields:
    #    filter.form.fields[field].widget = forms.BootstrapSelect(choices=self.CHOICES,
    #                               attrs={'data-live-search': 'true'})

    table = myTable(filter.qs)
    RequestConfig(request).configure(table)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('{}.{}'.format(mymodel.table_name, export_format))

    table.paginate(page=request.GET.get('page', 1), per_page=request.GET.get('per_page', 10))
    table.export_formats = ['csv', 'xls', 'json', 'tsv']

    return render(request, 'bns_landscape_query.html', {'table': table, 'filter': filter, 'landscape_name': landscape_name})