from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

from Biotics.profiles.validators import check_string_contains_only_letters, age_validator


# Create your models here.


class BioticsUserModel(AbstractUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Other'),
    ]

    BIOLOGY_CHOICES = [
        ('Botany', 'Botany'),
        ('Microbiology', 'Microbiology'),
        ('Zoology', 'Zoology'),
    ]

    RANK_CHOICES = [
        ('Student', 'Student'),
        ('Assistant', 'Assistant'),
        ('Associate Professor', 'Associate Professor'),
        ('Professor', 'Professor'),
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
    profile_picture = models.ImageField(blank=True, upload_to='profile_pics/')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=13, blank=True)
    biology_type = models.CharField(choices=BIOLOGY_CHOICES, max_length=13, blank=True)
    rank = models.CharField(choices=RANK_CHOICES, max_length=20, blank=True)
    age = models.PositiveIntegerField(default=18, blank=True, null=True, validators=[age_validator])

    def get_user_name(self):
        if self.first_name and self.last_name:
            return self.first_name + ' ' + self.last_name
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name
        else:
            return self.username


