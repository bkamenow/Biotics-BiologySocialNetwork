from django.core.validators import MinLengthValidator
from django.db import models

from Biotics.profiles.models import BioticsUserModel
from Biotics.publications.validators import validate_file_size


class PublicationModel(models.Model):
    TYPE_CHOICES = [
        ('Botany', 'Botany'),
        ('Microbiology', 'Microbiology'),
        ('Zoology', 'Zoology'),
    ]

    photo = models.ImageField(upload_to='publication_pics/', validators=(validate_file_size,))
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=300, validators=(MinLengthValidator(10),), blank=True, null=True)
    date_of_publication = models.DateField(auto_now=True)
    type_of_publication = models.CharField(choices=TYPE_CHOICES, max_length=13, blank=True)
    user = models.ForeignKey(to=BioticsUserModel, on_delete=models.CASCADE, related_name='publications')
    likes_count = models.PositiveIntegerField(default=0)

    def user_has_liked(self, user):
        return self.like_set.filter(user=user).exists()


class Like(models.Model):
    publication = models.ForeignKey(PublicationModel, on_delete=models.CASCADE)
    user = models.ForeignKey(BioticsUserModel, on_delete=models.CASCADE)


class Comment(models.Model):
    publication = models.ForeignKey(PublicationModel, on_delete=models.CASCADE)
    user = models.ForeignKey(BioticsUserModel, on_delete=models.CASCADE)
    content = models.TextField(validators=[MinLengthValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
