# Generated by Django 4.2.3 on 2023-08-01 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trainings', '0002_remove_trainingmodel_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_amount', models.PositiveIntegerField()),
                ('payment_method', models.CharField(max_length=50)),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainings.trainingmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]