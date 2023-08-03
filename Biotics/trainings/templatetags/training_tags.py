from django import template
from Biotics.trainings.models import Payment

register = template.Library()


@register.filter
def has_paid_for_training(user, training):
    try:
        payment = Payment.objects.get(user=user, training=training)
        return True
    except Payment.DoesNotExist:
        return False
