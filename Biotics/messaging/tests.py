from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import MessageForm
from .models import Conversation, Message

BioticsUserModel = get_user_model()


class ConversationModelTest(TestCase):
    def setUp(self):
        self.user1 = BioticsUserModel.objects.create_user(username='bobi1', email='bobi1@example.com',
                                                          password='bobi123')
        self.user2 = BioticsUserModel.objects.create_user(username='bobi2', email='bobi2@example.com',
                                                          password='bobi123')

    def test_get_other_user(self):
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1)
        conversation.participants.add(self.user2)

        other_user1 = conversation.get_other_user(self.user1)
        other_user2 = conversation.get_other_user(self.user2)

        self.assertEqual(other_user1, self.user2)
        self.assertEqual(other_user2, self.user1)


class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = BioticsUserModel.objects.create_user(username='bobi1', email='bobi1@example.com',
                                                          password='bobi123')
        self.user2 = BioticsUserModel.objects.create_user(username='bobi2', email='bobi2@example.com',
                                                          password='bobi123')
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1)
        self.conversation.participants.add(self.user2)

    def test_create_message(self):
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content='Hello, user2!'
        )
        message.receiver.add(self.user2)

        self.assertEqual(message.conversation, self.conversation)
        self.assertEqual(message.sender, self.user1)
        self.assertTrue(self.user2 in message.receiver.all())
        self.assertEqual(message.content, 'Hello, user2!')
        self.assertFalse(message.is_read)


class MessageFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'content': 'This is a test message.'
        }
        form = MessageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_content(self):
        form_data = {
            'content': ''
        }
        form = MessageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(form.errors['content'][0], 'This field is required.')

    def test_form_labels(self):
        form = MessageForm()
        self.assertEqual(form.fields['content'].label, '')

    def test_form_placeholder(self):
        form = MessageForm()
        self.assertEqual(form.fields['content'].widget.attrs['placeholder'], 'Type your message here...')


class ConversationViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = BioticsUserModel.objects.create_user(username='bobi1', email='bobi1@example.com', password='bobi123')
        self.user2 = BioticsUserModel.objects.create_user(username='bobi2', email='bobi2@example.com', password='bobi123')
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)
        self.url = reverse('conversation_view', args=[self.user2.id])

    def test_conversation_view_authenticated(self):
        self.client.login(username='bobi1', password='bobi123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'messaging/conversation_view.html')

    def test_send_message_authenticated(self):
        self.client.login(username='bobi1', password='bobi123')
        response = self.client.post(self.url, {'content': 'Hello'})
        self.assertEqual(response.status_code, 200)  # Assuming you're returning the same page after sending a message
        self.assertTrue(Message.objects.filter(conversation=self.conversation, sender=self.user1, content='Hello').exists())
