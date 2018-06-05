from django.urls import path
from . import views

urlpatterns = [
    # ex: /bns/
    path('', views.index, name='index'),

    # ex: /bns/surveys/
    path('surveys/', views.surveys, name='surveys'),

    # ex: /bns/surveys/bateke_2017/
    path('surveys/<str:survey_name>/', views.survey, name='survey'),

    # ex: /bns/surveys/bateke_2017/ame_per_hh/
    path('surveys/<str:survey_name>/<query_name>', views.query, name='query'),

]