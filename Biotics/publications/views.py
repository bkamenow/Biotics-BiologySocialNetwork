from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from Biotics.publications.forms import PublicationCreateForm, PublicationEditForm
from Biotics.publications.models import PublicationModel


class PublicationListView(LoginRequiredMixin, ListView):
    model = PublicationModel
    template_name = 'publications/publications.html'
    context_object_name = 'all_publications'


class PublicationCreateView(LoginRequiredMixin, CreateView):
    model = PublicationModel
    template_name = 'publications/create-publication.html'
    form_class = PublicationCreateForm
    success_url = reverse_lazy('publications')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PublicationUpdateView(LoginRequiredMixin, UpdateView):
    model = PublicationModel
    template_name = 'publications/edit-publication.html'
    form_class = PublicationEditForm

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PublicationDetailView(DetailView):
    model = PublicationModel
    template_name = 'publications/details-publication.html'
    context_object_name = 'publication'


class PublicationDeleteView(LoginRequiredMixin, DeleteView):
    model = PublicationModel
    template_name = 'publications/delete-publication.html'

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.object.user.pk})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publication'] = self.object
        return context
