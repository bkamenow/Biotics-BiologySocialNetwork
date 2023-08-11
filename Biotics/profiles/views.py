from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404

from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.views.generic import DeleteView

from Biotics.events.models import EventModel
from Biotics.messaging.models import Conversation
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
        logged_in_user = self.request.user
        conversations = Conversation.objects.filter(participants=logged_in_user) | Conversation.objects.filter(
            participants=self.object)

        other_users = [conversation.participants.exclude(id=logged_in_user.id).first() for conversation in
                       conversations]
        other_user = self.object

        followers_count = self.object.total_followers
        following_count = self.object.get_following_count

        paid_trainings = TrainingModel.objects.filter(payment__user=logged_in_user)
        total_publications = self.object.publications.count()
        context.update({
            'total_publications': total_publications,
            'other_users': other_users,
            'other_user': other_user,
            'paid_trainings': paid_trainings,
            'followers_count': followers_count,
            'following_count': following_count,
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


@login_required
def toggle_follow(request, username):
    user_to_toggle = get_object_or_404(BioticsUserModel, username=username)
    current_user = request.user
    following = user_to_toggle.following.all()

    if username != current_user.username:
        if current_user in following:
            user_to_toggle.following.remove(current_user.id)
        else:
            user_to_toggle.following.add(current_user.id)

    return redirect(reverse('profile_details', kwargs={'pk': user_to_toggle.pk}))

