# Generated by Django 4.2.3 on 2023-07-27 19:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publications', '0002_alter_publicationmodel_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publications', to=settings.AUTH_USER_MODEL),
        ),
    ]
