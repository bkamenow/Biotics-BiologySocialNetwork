from django.shortcuts import redirect
from django.urls import reverse


class PreventAuthUserAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            if request.path in [reverse('login_page'), reverse('create_profile')]:
                return redirect('home_page')

        if not request.user.is_superuser:
            if request.path in [reverse('create_training'), reverse('approval-event')]:
                return redirect('home_page')

        return response
