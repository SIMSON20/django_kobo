from django.urls import path
from . import views

app_name = 'kobo'

urlpatterns = [
    # ex /kobo/
    path('', views.index, name='index'),
    # ex: /kobo/bns_lsa/
    path('<str:auth_user>/', views.detail, name='detail'),

]