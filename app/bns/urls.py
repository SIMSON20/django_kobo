from django.urls import path
from . import views

urlpatterns = [
    # ex: /bns/
    path('', views.index, name='bns_index'),

    # ex: /bns/surveys/
    path('surveys/', views.surveys, name='bns_surveys'),

    # ex: /bns/surveys/bateke_2017/
    path('surveys/<str:survey_name>/', views.survey, name='bns_survey'),

    # ex: /bns/surveys/bateke_2017/ame_per_hh/
    path('surveys/<str:survey_name>/<query_name>', views.survey_query, name='bns_survey_query'),

    # ex: /bns/landscapes/
    path('landscapes/', views.landscapes, name='bns_landscapes'),

    # ex: /bns/landscapes/bateke
    path('landscapes/<str:landscape_name>/', views.landscape, name='bns_landscape'),

    # ex: /bns/landscapes/bateke/ame_per_hh/
    path('landscapes/<str:landscape_name>/<query_name>', views.landscape_query, name='bns_landscape_query'),

]