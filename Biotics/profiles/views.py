from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from Biotics.profiles.forms import BioticsUserCreateForm
from Biotics.profiles.models import BioticsUserModel


# Create your views here.


class BioticsUserRegisterView(views.CreateView):
    model = BioticsUserModel
    form_class = BioticsUserCreateForm
    template_name = 'profiles/profile-create.html'
    success_url = reverse_lazy('login_page')


def edit_profile(request):
    return render(request, template_name='profiles/profile-edit.html')


def delete_profile(request):
    return render(request, template_name='profiles/profile-delete.html')


def profile_details(request):
    return render(request, template_name='profiles/profile-details.html')
