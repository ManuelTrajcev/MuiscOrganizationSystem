from django.shortcuts import redirect
from django.http import Http404

class Redirect404ToHomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Http404:
            return redirect('homepage')
