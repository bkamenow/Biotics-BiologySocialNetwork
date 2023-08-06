from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import BioticsUserModel


@receiver(post_save, sender=BioticsUserModel)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our App!'
        context = {'user': instance}
        html_message = render_to_string('profiles/welcome_email.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'kamenowink@gmail.com'
        to_email = instance.email
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
