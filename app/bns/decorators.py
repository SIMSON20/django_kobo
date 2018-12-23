from django.shortcuts import redirect
from .models import Answer


def has_survey_access(function=None):
    """Check that the user has access to a survey

    This decorator ensures that the view functions it is called on can be
    accessed only by users with appropriate permissions.
    All other users are redirected to an Access denied page.
    """

    def _dec(view_func):
        def _view(request, *args, **kwargs):

            user = request.user
            dataset_name = kwargs["survey_name"]
            query_name = kwargs["query_name"]

            if 'landscape' in query_name.lower() or \
                    (user.is_authenticated and
                     (user.is_superuser or
                      dataset_name in [s.dataset_name for s in user.kobouser.surveys.order_by('dataset_name')])):
                return view_func(request, *args, **kwargs)
            else:
                return redirect('access-denied')

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)


def has_landscape_access(function=None):
    """Check that the user has access to a survey

    This decorator ensures that the view functions it is called on can be
    accessed only by users with appropriate permissions.
    All other users are redirected to an Access denied page.
    """

    def _dec(view_func):
        def _view(request, *args, **kwargs):

            user = request.user
            landscape_name = kwargs["landscape_name"]
            query_name = kwargs["query_name"]

            if 'landscape' in query_name.lower():
                return view_func(request, * args, ** kwargs)

            elif user.is_authenticated:

                surveys = [s.dataset_uuid for s in user.kobouser.surveys.all()]
                landscapes = Answer.objects.filter(dataset_uuid_id__in=surveys).only('landscape').order_by(
                    'landscape').distinct('landscape')
                landscape_names = list()

                for landscape in landscapes:
                    landscape_names.append(landscape.landscape)

                if user.is_superuser or landscape_name in landscape_names:
                    kwargs["surveys"] = surveys
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('access-denied')
            else:
                return redirect('access-denied')

        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)
