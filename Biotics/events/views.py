from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from Biotics.events.forms import EventForm
from Biotics.events.models import EventModel


# Create your views here.


class EventListView(ListView):
    model = EventModel
    template_name = 'events/events.html'
    context_object_name = 'events'
    paginate_by = 10


class EventCreateView(LoginRequiredMixin, CreateView):
    model = EventModel
    form_class = EventForm
    template_name = 'events/create-event.html'
    success_url = reverse_lazy('events')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = EventModel
    form_class = EventForm
    template_name = 'events/edit-event.html'
    context_object_name = 'event'
    success_url = reverse_lazy('events')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class EventDetailView(DetailView):
    model = EventModel
    template_name = 'events/details-event.html'
    context_object_name = 'all_events'


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = EventModel
    template_name = 'events/delete-event.html'
    success_url = reverse_lazy('events')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
