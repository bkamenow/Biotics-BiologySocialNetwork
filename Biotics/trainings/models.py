from django.core.validators import MinLengthValidator
from django.db import models

from Biotics.profiles.models import BioticsUserModel
from Biotics.publications.validators import validate_file_size


class TrainingModel(models.Model):
    TYPE_CHOICES = [
        ('Botany', 'Botany'),
        ('Microbiology', 'Microbiology'),
        ('Zoology', 'Zoology'),
    ]

    photo = models.ImageField(upload_to='training_pics/', validators=(validate_file_size,))
    title = models.CharField(max_length=30, blank=False, null=False)
    description = models.TextField(max_length=300, validators=(MinLengthValidator(10),), blank=False, null=False)
    price = models.PositiveIntegerField(blank=False, null=False)
    date_of_training = models.DateField(auto_now=True)
    type_of_training = models.CharField(choices=TYPE_CHOICES, max_length=13, blank=False, null=False)

    def __str__(self):
        return self.title


class Payment(models.Model):
    user = models.ForeignKey(BioticsUserModel, on_delete=models.CASCADE)
    training = models.ForeignKey(TrainingModel, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_amount = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment for {self.training.title} on {self.payment_date}"

