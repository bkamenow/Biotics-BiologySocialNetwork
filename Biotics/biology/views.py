from django.shortcuts import render

# Create your views here.


def zoology_home(request):
    return render(request, template_name='biology/zoology-home.html')


def botany_home(request):
    return render(request, template_name='biology/botany.html')


def microbiology_home(request):
    return render(request, template_name='biology/microbiology.html')

