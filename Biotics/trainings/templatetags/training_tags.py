from django import template
from Biotics.trainings.models import Payment

register = template.Library()


@register.filter(name='has_paid_for_training')
def has_paid_for_training(user, training):
    return Payment.objects.filter(user=user, training=training).exists()
