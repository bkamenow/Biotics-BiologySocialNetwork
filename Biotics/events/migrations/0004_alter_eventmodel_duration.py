# Generated by Django 4.2.3 on 2023-07-30 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_eventmodel_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventmodel',
            name='duration',
            field=models.CharField(),
        ),
    ]
