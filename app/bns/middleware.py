from django.http import HttpResponseRedirect
from django.urls import reverse


class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        split_path = request.path.split('/')
        if "bns" in split_path and ("survey" in split_path or "surveys" in split_path or "landscape" in split_path or "landscapes" in split_path):
            if not request.user.is_authenticated:
                # TODO: replace login page with social Auth login
                return HttpResponseRedirect(reverse('login')) # or http response
        return self.get_response(request)
