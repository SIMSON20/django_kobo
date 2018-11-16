from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings
import urllib


register = template.Library()

@register.filter
@stringfilter
def strip_lang(value):
    """Removes all values of arg from the given string"""
    lang = getattr(settings, "LANGUAGES", None)
    url = value.split('/')
    if url[1] in [l[0] for l in lang]:
        return urllib.parse.unquote('/' + '/'.join(value.split('/')[2:]))
    else:
        return urllib.parse.unquote(value)

