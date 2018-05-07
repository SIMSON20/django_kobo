from django.contrib import admin

from .models import AME
from .models import Answer, AnswerGPS, AnswerGS, AnswerHHMembers, AnswerNR

admin.site.register(AME)


class AnswerGPSInline(admin.StackedInline):
    model = AnswerGPS


class AnswerGSInline(admin.StackedInline):
    model = AnswerGS
    extra = 1


class AnswerHHMembersInline(admin.StackedInline):
    model = AnswerHHMembers
    extra = 1


class AnswerNRInline(admin.StackedInline):
    model = AnswerNR
    extra = 1


class AnswerAdmin(admin.ModelAdmin):
    inlines = [AnswerGPSInline, AnswerGSInline, AnswerHHMembersInline, AnswerNRInline]


admin.site.register(Answer, AnswerAdmin)