# Generated by Django 4.2.4 on 2023-08-07 17:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0004_alter_eventmodel_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmodel',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='joined_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
