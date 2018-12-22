from django.contrib import admin
from .models import Answer, Price


class AnswerLandscapeFilter(admin.SimpleListFilter):

    """
    This filter will always return a subset of the instances in a Model, either filtering by the
    user choice or by a default value.
    """
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'landscape'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'landscape'

    default_value = None

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        landscape_list = list()
        queryset = Answer.objects.defer("landscape").order_by('landscape').distinct('landscape')

        if not request.user.is_superuser:
            surveys = [s.dataset_uuid for s in request.user.kobouser.surveys.all()]
            landscapes = Answer.objects.filter(dataset_uuid_id__in=surveys).only('landscape').order_by(
                'landscape').distinct('landscape')
            landscape_names = list()

            for landscape in landscapes:
                landscape_names.append(landscape.landscape)
            queryset = queryset.filter(landscape__in=landscape_names)

        for answer in queryset:
            landscape_list.append((answer.landscape, answer.landscape))
        return landscape_list

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(landscape__exact=self.value())
        return queryset


class SubAnswerLandscapeFilter(AnswerLandscapeFilter):

    """
    This filter will always return a subset of the instances in a Model, either filtering by the
    user choice or by a default value.
    """

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(answer__landscape__exact=self.value())
        return queryset


class PriceAnswerLandscapeFilter(AnswerLandscapeFilter):

    """
    This filter will always return a subset of the instances in a Model, either filtering by the
    user choice or by a default value.
    """

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(dataset_uuid__answer__landscape__exact=self.value())
        return queryset


class AnswerSurveyFilter(admin.SimpleListFilter):
    """
    This filter is an example of how to combine two different Filters to work together.
    """
    # Human-readable title which will be displayed in the right admin sidebar just above the filter
    # options.
    title = 'survey'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'survey'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        survey_list = []
        queryset = Answer.objects.defer("dataset_uuid_id", "dataset_uuid__dataset_name", "landscape")\
                                    .order_by("dataset_uuid__dataset_name", "dataset_uuid", "landscape")\
                                    .distinct("dataset_uuid__dataset_name", "dataset_uuid", "landscape")

        if not request.user.is_superuser:
            surveys = [s.dataset_uuid for s in request.user.kobouser.surveys.all()]
            queryset = queryset.filter(dataset_uuid_id__in=surveys)

        if 'landscape' in request.GET:
            queryset = queryset.filter(landscape=request.GET['landscape'])

        for survey in queryset.values("dataset_uuid_id", "dataset_uuid__dataset_name", "landscape"):
            survey_list.append((survey["dataset_uuid_id"], survey["dataset_uuid__dataset_name"]))

        return survey_list

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(dataset_uuid=self.value())
        return queryset


class SubAnswerSurveyFilter(AnswerSurveyFilter):
    """
    This filter is an example of how to combine two different Filters to work together.
    """

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(answer__dataset_uuid=self.value())
        return queryset


class AnswerVillageFilter(admin.SimpleListFilter):
    """
    This filter is an example of how to combine two different Filters to work together.
    """
    # Human-readable title which will be displayed in the right admin sidebar just above the filter
    # options.
    title = 'village'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'village'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        survey_list = []
        queryset = Answer.objects.defer("dataset_uuid_id", "landscape", "village")\
                                    .order_by("village")\
                                    .distinct("village")

        if 'landscape' in request.GET:
            queryset = queryset.filter(landscape=request.GET['landscape'])

        if 'survey' in request.GET:
            queryset = queryset.filter(dataset_uuid_id=request.GET['survey'])

        if not request.user.is_superuser:
            surveys = [s.dataset_uuid for s in request.user.kobouser.surveys.all()]
            queryset = queryset.filter(dataset_uuid_id__in=surveys)

        for survey in queryset:
            survey_list.append((survey.village, survey.village))

        return survey_list

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(village=self.value())
        return queryset


class SubAnswerVillageFilter(AnswerVillageFilter):
    """
    This filter is an example of how to combine two different Filters to work together.
    """

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(answer__village=self.value())
        return queryset


class PriceAnswerVillageFilter(admin.SimpleListFilter):
    """
    This filter is an example of how to combine two different Filters to work together.
    """
    # Human-readable title which will be displayed in the right admin sidebar just above the filter
    # options.
    title = 'village'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'village'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        survey_list = []
        queryset = Price.objects.defer("dataset_uuid_id", "dataset_uuid__answer__landscape", "village")\
                                    .order_by("village")\
                                    .distinct("village")

        if 'landscape' in request.GET:
            queryset = queryset.filter(dataset_uuid__answer__landscape=request.GET['landscape'])

        if 'survey' in request.GET:
            queryset = queryset.filter(dataset_uuid_id=request.GET['survey'])

        if not request.user.is_superuser:
            surveys = [s.dataset_uuid for s in request.user.kobouser.surveys.all()]
            queryset = queryset.filter(dataset_uuid_id__in=surveys)

        for survey in queryset:
            survey_list.append((survey.village, survey.village))

        return survey_list

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(village=self.value())
        return queryset
