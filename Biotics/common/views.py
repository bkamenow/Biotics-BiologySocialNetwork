from django.shortcuts import render
from django.views.defaults import page_not_found

# Create your views here.


def home_page(request):
    return render(request, template_name='common/home.html')


def page_not_found_view(request, exception):
    return render(request, template_name='404.html', status=404)


def trainings_page(request):
    return render(request, template_name='common/trainings.html')


def events_page(request):
    return render(request, template_name='common/events.html')