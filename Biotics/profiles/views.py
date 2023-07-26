from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.views.generic import DeleteView

from Biotics.profiles.forms import BioticsUserCreateForm, LoginForm, BioticsUserEditForm
from Biotics.profiles.models import BioticsUserModel


class BioticsUserRegisterView(views.CreateView):
    model = BioticsUserModel
    form_class = BioticsUserCreateForm
    template_name = 'profiles/profile-create.html'
    success_url = reverse_lazy('login_page')


class BioticsUserLoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'profiles/login.html'
    next_page = reverse_lazy('home_page')


class BioticsUserLogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('login_page')


class BioticsUserDetailsView(views.DetailView):
    model = BioticsUserModel
    template_name = 'profiles/profile-details.html'


class BioticsUserEditView(views.UpdateView):
    model = BioticsUserModel
    form_class = BioticsUserEditForm
    template_name = 'profiles/profile-edit.html'

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.object.pk})


class BioticsUserDeleteView(LoginRequiredMixin, DeleteView):
    model = BioticsUserModel
    template_name = 'profiles/profile-delete.html'
    success_url = reverse_lazy('home_page')

    def get_object(self, queryset=None):
        return self.request.user
