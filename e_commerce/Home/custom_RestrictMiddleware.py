from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse

class CustomRestrictAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        allowed_urls = [reverse("home"), reverse("session"), reverse("login")]
        if request.path in allowed_urls:
            return self.get_response(request)

        if not request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_URL)

        return response