from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.views.generic import DeleteView

from Biotics.profiles.forms import BioticsUserCreateForm, LoginForm, BioticsUserEditForm, CustomPasswordResetForm
from Biotics.profiles.models import BioticsUserModel
from Biotics.trainings.models import TrainingModel, Payment


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_publications = self.object.publications.count()
        context.update({
            'total_publications': total_publications,
        })
        return context


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


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'password_reset/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'password_reset/password_reset_done.html'


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password_reset/password_reset_complete.html'
