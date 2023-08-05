# Generated by Django 4.2.3 on 2023-08-01 19:43

import Biotics.publications.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0003_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingmodel',
            name='photo',
            field=models.ImageField(upload_to='training_pics/', validators=[Biotics.publications.validators.validate_file_size]),
        ),
    ]
