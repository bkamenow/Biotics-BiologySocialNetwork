import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from Biotics.trainings.forms import TrainingCreateForm, TrainingEditForm, PaymentForm
from Biotics.trainings.models import TrainingModel


# Create your views here.


class TrainingListView(LoginRequiredMixin, ListView):
    model = TrainingModel
    template_name = 'trainings/trainings.html'
    context_object_name = 'all_trainings'


class TrainingCreateView(LoginRequiredMixin, CreateView):
    model = TrainingModel
    template_name = 'trainings/create-training.html'
    form_class = TrainingCreateForm
    success_url = reverse_lazy('trainings')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TrainingUpdateView(LoginRequiredMixin, UpdateView):
    model = TrainingModel
    template_name = 'trainings/edit-training.html'
    form_class = TrainingEditForm

    def get_success_url(self):
        return reverse_lazy('trainings')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TrainingDeleteView(LoginRequiredMixin, DeleteView):
    model = TrainingModel
    template_name = 'trainings/delete-training.html'

    def get_success_url(self):
        return reverse_lazy('trainings')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['training'] = self.object
        return context


def handle_stripe_error(error, form):
    error_msg = error.user_message or "An error occurred while processing your payment. Please try again later."
    form.add_error(None, error_msg)


def join_training(request, pk):
    training = get_object_or_404(TrainingModel, pk=pk)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['stripe_token']

            try:
                stripe.api_key = settings.STRIPE_SECRET_KEY
                charge = stripe.Charge.create(
                    amount=training.price * 100,
                    currency='usd',
                    description='Join Training Payment',
                    source={'token': token},
                )

                return redirect('success_url')
            except stripe.error.StripeError as e:
                handle_stripe_error(e, form)
    else:
        form = PaymentForm()

    return render(request, 'trainings/payment_form.html', {'form': form, 'training': training})
