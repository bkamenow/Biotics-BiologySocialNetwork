from django.db import models

from Biotics.profiles.models import BioticsUserModel


class Conversation(models.Model):
    participants = models.ManyToManyField(BioticsUserModel, related_name='conversations')

    def get_other_user(self, user):
        return self.participants.exclude(id=user.id).first()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(BioticsUserModel, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ManyToManyField(BioticsUserModel, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
