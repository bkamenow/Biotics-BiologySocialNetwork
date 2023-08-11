import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from Biotics.profiles.models import BioticsUserModel
from Biotics.trainings.forms import TrainingCreateForm, TrainingEditForm
from Biotics.trainings.models import TrainingModel, Payment


class TrainingListView(LoginRequiredMixin, ListView):
    model = TrainingModel
    template_name = 'trainings/trainings.html'
    context_object_name = 'all_trainings'
    login_url = reverse_lazy('login_page')

    def get_queryset(self):
        return TrainingModel.objects.order_by('-date_of_training')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['all_trainings'], 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['all_trainings'] = page_obj

        return context


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

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'bgn',
                    'unit_amount': int(training.price * 100),
                    'product_data': {
                        'name': training.title,
                    },
                },
                'quantity': 1,
            },
        ],
        payment_intent_data={'metadata': {
            'training_id': str(training.id),
            'client_reference_id': str(user.id),
        },
        },
        mode='payment',
        success_url=request.build_absolute_uri(reverse('trainings')),
    )
    return redirect(session.url)


@csrf_exempt
def stripe_webhook(request):
    if request.method == 'POST':
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return JsonResponse({'error': str(e)}, status=400)

        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            training_id = payment_intent['metadata'].get('training_id')
            user_id = payment_intent['metadata'].get('client_reference_id')

            if training_id is None or user_id is None:
                print("Training ID or User ID is missing in metadata")
                print(payment_intent['metadata'])
                return JsonResponse({'status': 'error', 'message': 'Training ID or User ID is missing in metadata'},
                                    status=400)

            try:
                training = TrainingModel.objects.get(id=training_id)
                user = BioticsUserModel.objects.get(id=user_id)
                payment_amount = payment_intent['amount_received'] / 100  # Use 'amount_received' instead of 'amount'

                payment = Payment.objects.create(
                    training=training,
                    user=user,
                    amount=payment_amount,
                )
            except (TrainingModel.DoesNotExist, BioticsUserModel.DoesNotExist):
                print(f"Training or User does not exist - training_id: {training_id}, user_id: {user_id}")
                return JsonResponse({'status': 'error', 'message': 'Training or User does not exist'}, status=400)

    return JsonResponse({'status': 'success'})
