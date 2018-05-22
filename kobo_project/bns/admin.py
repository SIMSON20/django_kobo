from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import AME
from .models import Answer, AnswerGPS, AnswerGS, AnswerHHMembers, AnswerNR


@admin.register(AME)
class AMEAdmin(ImportExportModelAdmin):
    pass


@admin.register(AnswerGPS)
class AnswerGPSAdmin(ImportExportModelAdmin):
    pass


class AnswerGPSInline(admin.StackedInline):
    model = AnswerGPS


@admin.register(AnswerGS)
class AnswerGSAdmin(ImportExportModelAdmin):
    pass


class AnswerGSInline(admin.StackedInline):
    model = AnswerGS
    extra = 1


@admin.register(AnswerHHMembers)
class AnswerHHMembersAdmin(ImportExportModelAdmin):
    pass


class AnswerHHMembersInline(admin.StackedInline):
    model = AnswerHHMembers
    extra = 1


@admin.register(AnswerNR)
class AnswerNRAdmin(ImportExportModelAdmin):
    pass


class AnswerNRInline(admin.StackedInline):
    model = AnswerNR
    extra = 1


@admin.register(Answer)
class AnswerAdmin(ImportExportModelAdmin):
    """
    Admin class for Connections
    """
    #list_display = ['dataset_id']
    inlines = [AnswerGPSInline, AnswerGSInline, AnswerHHMembersInline, AnswerNRInline]

