from django.urls import path
from . import views


urlpatterns = [
    # ex: /nrgt/
    path('', views.index, name='index'),

    # ex: /nrgt/surveys/
    path('surveys/', views.nrgt_surveys, name='nrgt_surveys'),

    # ex: /nrgt/surveys/bateke_2017/
    path('surveys/<str:survey_name>/', views.survey, name='survey'),

    # ex: /nrgt/surveys/bateke_2017/ame_per_hh/
    path('surveys/<str:survey_name>/<query_name>', views.survey_query, name='survey_query'),

    # ex: /nrgt/landscapes/
    path('landscapes/', views.landscapes, name='landscapes'),

    # ex: /nrgt/landscapes/bateke
    path('landscapes/<str:landscape_name>/', views.landscape, name='landscape'),

    # ex: /nrgt/landscapes/bateke/ame_per_hh/
    path('landscapes/<str:landscape_name>/<query_name>', views.landscape_query, name='landscape_query'),

]