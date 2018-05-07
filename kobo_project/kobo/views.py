from django.shortcuts import get_object_or_404, render
from django.http import Http404

from .models import Connection


def index(request):
    connection_list = Connection.objects.order_by('-auth_user')[:5]

    context = {
        'connection_list': connection_list,
    }
    return render(request, 'kobo/index.html', context)


def detail(request, auth_user):
    connection = get_object_or_404(Connection, auth_user=auth_user)
    return render(request, 'kobo/detail.html', {'connection': connection})
