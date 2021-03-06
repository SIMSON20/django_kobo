"""kobo_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.conf.urls.i18n import i18n_patterns

admin.site.site_header = 'CARPE Surveys Administration'
admin.site.index_title = 'Site administration'
admin.site.site_title = 'CARPE Surveys site admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    ]

urlpatterns += i18n_patterns(
    path('nrgt/', include('nrgt.urls')),
    path('bns/', include('bns.urls')),
    path('kobo/', include('kobo.urls')),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^access-denied/$', TemplateView.as_view(template_name='access_denied.html'), name='access-denied'),
    url(r'^login/$', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    prefix_default_language=False)

