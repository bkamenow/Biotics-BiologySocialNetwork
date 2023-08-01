# Generated by Django 4.2.3 on 2023-08-01 17:03

import Biotics.publications.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='events_pics/', validators=[Biotics.publications.validators.validate_file_size])),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=300, validators=[django.core.validators.MinLengthValidator(10)])),
                ('price', models.PositiveIntegerField()),
                ('date_of_training', models.DateField(auto_now=True)),
                ('type_of_training', models.CharField(choices=[('Botany', 'Botany'), ('Microbiology', 'Microbiology'), ('Zoology', 'Zoology')], max_length=13)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
