from .admin import sync_connection
from .models import Connection


def check_for_updates():

  queryset = Connection.objects.all()
  sync_connection(queryset)
