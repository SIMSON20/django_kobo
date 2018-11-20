from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Connection, KoboData
from .resources import KoboDataFromFileResource
from .management.commands._actions import sync


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    """
    Admin class for Connections
    """
    list_display = ['auth_user', 'host_assets', 'last_update_time']
    ordering = ['auth_user']

    def sync(self, request, queryset):
        """
        Add action to fetch latest data from Kobo
        :param request:
        :param queryset:
        :return:
        """

        sync(queryset)

        self.message_user(request, "Data successfully updated")

    actions = [sync]
    sync.short_description = "Sync data"


@admin.register(KoboData)
class KoboDataAdmin(ImportExportModelAdmin):
    list_display = ['dataset_name', 'dataset_year', 'tags', 'dataset_owner', 'last_submission_time', 'last_update_time', 'last_checked_time', 'kobo_managed']
    ordering = ['dataset_owner', 'dataset_name', 'dataset_year']
    resource_class = KoboDataFromFileResource
