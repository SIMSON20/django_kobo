from django.urls import path

from . import views

urlpatterns = [
    # ex: /bns/
    path('', views.index, name='index'),
    # ex: /bns/ame_per_hh/
    path('query/<str:query_name>/', views.query, name='query'),
]