from django import template

register = template.Library()


@register.simple_tag
def get_user_surveys(user):
    if not user.is_authenticated:
        return list()
    else:
        return [s.dataset_name for s in user.kobouser.surveys.order_by('dataset_name')]
