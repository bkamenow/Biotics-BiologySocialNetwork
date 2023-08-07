import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from Biotics.trainings.forms import TrainingCreateForm, TrainingEditForm
from Biotics.trainings.models import TrainingModel, Payment


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


stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def initiate_payment(request, pk):
    training = get_object_or_404(TrainingModel, pk=pk)
    user = request.user

    payment = Payment.objects.create(
        training=training,
        user=user,
        amount=training.price,
    )
    return redirect('https://buy.stripe.com/test_bIY17s3QI3zy7DybII')


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        training_id = session.metadata.get('training_id')
        if training_id:
            try:
                training = TrainingModel.objects.get(id=training_id)
                payment = Payment.objects.create(
                    training=training,
                    user=request.user,
                    amount=session.amount_total / 100,

                )
            except TrainingModel.DoesNotExist:
                pass

    return JsonResponse({'status': 'success'})
