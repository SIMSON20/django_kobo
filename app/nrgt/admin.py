from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import NRGTAnswer


@admin.register(NRGTAnswer)
class NRGTAnswerAdmin(ImportExportModelAdmin):
    """
    Admin class for Connections
    """
    pass