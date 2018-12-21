from django import template
from bns.models import Answer

register = template.Library()


@register.simple_tag
def get_user_surveys(user):
    if not user.is_authenticated:
        return list()
    else:
        return [s.dataset_name for s in user.kobouser.surveys.order_by('dataset_name')]



@register.simple_tag
def get_user_landscapes(user):
    if not user.is_authenticated:
        return list()
    else:
        surveys = [s.dataset_uuid for s in user.kobouser.surveys.all()]
        landscapes = Answer.objects.filter(dataset_uuid_id__in=surveys).only('landscape').order_by(
            'landscape').distinct('landscape')
        landscape_names = list()

        for landscape in landscapes:
            landscape_names.append(landscape.landscape)

        return landscape_names
