from django.core.management.base import BaseCommand, CommandError
from ._actions import sync
from ...models import Connection


class Command(BaseCommand):
    help = 'update kobo forms for all connections'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        # Get all connections
        try:
            queryset = Connection.objects.all()
            sync(queryset)
        except:
            raise CommandError('Sync with Kobo Platform failed')

        self.stdout.write(self.style.SUCCESS('Successfully synced all data'))
