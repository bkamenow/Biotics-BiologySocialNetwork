from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

from Biotics.profiles.validators import check_string_contains_only_letters


# Create your models here.


class BioticsUserModel(AbstractUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Other'),
    ]

    BIOLOGY_CHOICES = [
        ('Bot', 'Botany'),
        ('Micro', 'Microbiology'),
        ('Zoo', 'Zoology'),
    ]

    RANK_CHOICES = [
        ('St', 'Student'),
        ('As', 'Assistant'),
        ('AP', 'Associate Professor'),
        ('Pr', 'Professor'),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30,
                                  blank=True,
                                  validators=[
                                      MinLengthValidator(2),
                                      check_string_contains_only_letters
                                  ])
    last_name = models.CharField(max_length=30,
                                 blank=True,
                                 validators=[
                                     MinLengthValidator(2),
                                     check_string_contains_only_letters
                                 ])
    profile_picture = models.ImageField(blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    biology_type = models.CharField(choices=BIOLOGY_CHOICES, max_length=10, blank=True)
    rank = models.CharField(choices=RANK_CHOICES, max_length=20, blank=True)

    def __str__(self):
        return self.email
