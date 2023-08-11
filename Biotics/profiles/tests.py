from django.test import TestCase

from django.contrib.auth.forms import AuthenticationForm

from django.core import mail
from django.core.exceptions import ValidationError

from django.urls import reverse

from .forms import BioticsUserCreateForm, CustomPasswordResetForm, BioticsUserEditForm
from .models import BioticsUserModel
from ..messaging.models import Conversation


class BioticsUserModelTest(TestCase):
    def setUp(self):
        self.user = BioticsUserModel.objects.create_user(
            username='bobi123',
            email='bobi1@example.com',
            first_name='bobi',
            last_name='kamenov',
            gender='Male',
            biology_type='Botany',
            rank='Student',
            age=25,
        )

    def test_user_creation(self):
        new_user = BioticsUserModel.objects.create_user(
            username='newuser',
            email='new@example.com',
            first_name='New',
            last_name='User',
            gender='Female',
            biology_type='Microbiology',
            rank='Professor',
            age=40,
        )

        self.assertEqual(new_user.username, 'newuser')
        self.assertEqual(new_user.email, 'new@example.com')
        self.assertEqual(new_user.first_name, 'New')
        self.assertEqual(new_user.last_name, 'User')
        self.assertEqual(new_user.gender, 'Female')
        self.assertEqual(new_user.biology_type, 'Microbiology')
        self.assertEqual(new_user.rank, 'Professor')
        self.assertEqual(new_user.age, 40)

    def test_user_age_validator(self):
        self.user.age = 30
        self.user.full_clean()

        with self.assertRaises(ValidationError):
            self.user.age = 17
            self.user.full_clean()

        self.user.age = 18
        self.user.full_clean()

    def test_followers_and_following_relationship(self):
        follower1 = BioticsUserModel.objects.create_user(username='follower1', email='follower1@example.com')
        follower2 = BioticsUserModel.objects.create_user(username='follower2', email='follower2@example.com')
        self.user.followers.add(follower1, follower2)

        self.assertEqual(self.user.followers.count(), 2)
        self.assertTrue(follower1 in self.user.followers.all())
        self.assertTrue(follower2 in self.user.followers.all())

        following_user = BioticsUserModel.objects.create_user(username='following', email='following@example.com')
        self.user.following.add(following_user)

        self.assertEqual(self.user.following.count(), 1)
        self.assertTrue(following_user in self.user.following.all())


class LoginFormTest(TestCase):
    def setUp(self):
        self.user = BioticsUserModel.objects.create_user(
            username='bobi123',
            email='bobi1@example.com',
            password='P@ssw0rd123',
        )

    def test_login_form_valid(self):
        form_data = {
            'username': 'bobi123',
            'password': 'P@ssw0rd123',
        }
        form = AuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_empty_fields(self):
        form_data = {
            'username': '',
            'password': '',
        }
        form = AuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)

    def test_login_form_missing_username(self):
        form_data = {
            'username': '',
            'password': 'P@ssw0rd123',
        }
        form = AuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertNotIn('password', form.errors)

    def test_login_form_missing_password(self):
        form_data = {
            'username': 'bobi123',
            'password': '',
        }
        form = AuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)
        self.assertNotIn('username', form.errors)

    def test_login_form_with_errors(self):
        form_data = {
            'username': 'bobi123',
            'password': 'wrongpassword',
        }
        form = AuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Please enter a correct username and password. Note that both fields may be case-sensitive.',
                      form.non_field_errors()
                      )


class BioticsUserCreateFormTest(TestCase):
    def test_biotics_user_create_form_valid(self):
        form_data = {
            'username': 'bobi123',
            'email': 'bobi1@example.com',
            'password1': 'P@ssw0rd123',
            'password2': 'P@ssw0rd123',
        }
        form = BioticsUserCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_biotics_user_create_form_invalid_password_mismatch(self):
        form_data = {
            'username': 'bobi123',
            'email': 'bobi1@example.com',
            'password1': 'P@ssw0rd123',
            'password2': 'DifferentPassword',
        }
        form = BioticsUserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_biotics_user_create_form_invalid_username_duplicate(self):
        BioticsUserModel.objects.create_user(
            username='bobi123',
            email='existing@example.com',
            password='P@ssw0rd123',
        )
        form_data = {
            'username': 'bobi123',
            'email': 'newemail@example.com',
            'password1': 'NewPassword123',
            'password2': 'NewPassword123',
        }
        form = BioticsUserCreateForm(data=form_data)
        self.assertFalse(form.is_valid())


class BioticsUserEditFormTest(TestCase):
    def setUp(self):
        self.user = BioticsUserModel.objects.create_user(
            username='bobi123',
            email='bobi1@example.com',
            password='P@ssw0rd123',
            first_name='Bobi',
            last_name='Kamenov',
            profile_picture=None,
            gender='Male',
            age=25,
            biology_type='Botany',
            rank='Student',
        )

    def test_biotics_user_edit_form_valid(self):
        form_data = {
            'username': 'newbobi123',
            'first_name': 'Gosho',
            'last_name': 'Armenov',
            'email': 'newemail@example.com',
            'profile_picture': None,
            'gender': 'Female',
            'age': 30,
            'biology_type': 'Zoology',
            'rank': 'Assistant',
        }
        form = BioticsUserEditForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_biotics_user_edit_form_invalid_email(self):
        form_data = {
            'username': 'newbobi123',
            'first_name': 'New First Name',
            'last_name': 'New Last Name',
            'email': 'invalidemail',  # Invalid email format
            'profile_picture': None,
            'gender': 'Female',
            'age': 30,
            'biology_type': 'Zoology',
            'rank': 'Assistant',
        }
        form = BioticsUserEditForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())


class CustomPasswordResetFormTest(TestCase):
    def setUp(self):
        self.user = BioticsUserModel.objects.create_user(username='testuser', email='testuser@example.com')

    def test_custom_password_reset_form_valid(self):
        form_data = {
            'email': 'testuser@example.com',
        }
        form = CustomPasswordResetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_custom_password_reset_form_invalid_email(self):
        form_data = {
            'email': 'invalidemail',  # Invalid email format
        }
        form = CustomPasswordResetForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_custom_password_reset_form_sends_email(self):
        form_data = {
            'email': 'testuser@example.com',
        }
        response = self.client.post(reverse('password_reset'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirects after form submission

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Welcome to Our App!')

    def test_custom_password_reset_form_does_not_send_email_with_invalid_data(self):
        mail.outbox = []
        form_data = {
            'email': 'invalidemail',
        }
        response = self.client.post(reverse('password_reset'), form_data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)


class BioticsUserRegisterViewTest(TestCase):
    def setUp(self):
        self.register_url = reverse('create_profile')
        self.form_data = {
            'username': 'bobi123',
            'email': 'bobi1@example.com',
            'password1': 'bobi123',
            'password2': 'bobi123',
        }

    def test_register_view_valid_form(self):
        response = self.client.post(self.register_url, data=self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BioticsUserModel.objects.count(), 1)

    def test_register_view_invalid_form(self):
        invalid_form_data = {
            'username': 'bobi123',
            'email': 'bobiexample.com',  # Invalid email format
            'password1': 'bobi123',
            'password2': 'bobi123',
        }
        response = self.client.post(self.register_url, data=invalid_form_data)
        self.assertEqual(response.status_code, 200)  # Form submission with errors
        self.assertEqual(BioticsUserModel.objects.count(), 0)  # User should not be created

    def test_register_view_redirects_to_login_page(self):
        response = self.client.get(self.register_url)
        self.assertTemplateUsed(response, 'profiles/profile-create.html')
        self.assertContains(response, 'Register')


class BioticsUserLoginViewTest(TestCase):
    def setUp(self):
        self.login_url = reverse('login_page')
        self.user = BioticsUserModel.objects.create_user(username='bobi111', email='bobi1@example.com', password='bobi123')
        self.form_data = {
            'username': 'bobi111',
            'password': 'bobi123',
        }

    def test_login_view_valid_credentials(self):
        response = self.client.post(self.login_url, data=self.form_data)
        self.assertRedirects(response, reverse('home_page'))  # Redirects after successful login

    def test_login_view_invalid_credentials(self):
        invalid_form_data = {
            'username': 'bobi1',
            'password': '123bobi',  # Invalid password
        }
        response = self.client.post(self.login_url, data=invalid_form_data)
        self.assertEqual(response.status_code, 200)  # Form submission with errors

    def test_login_view_template_used(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'profiles/login.html')
        self.assertContains(response, 'Login')


class BioticsUserDetailsViewTest(TestCase):
    def setUp(self):
        self.user = BioticsUserModel.objects.create_user(username='bobi1', email='bobi1@example.com', password='bobi123')
        self.other_user = BioticsUserModel.objects.create(username='bioticsuser', email='bioticsuser@example.com')
        self.details_url = reverse('profile_details', args=[self.other_user.pk])
        self.client.login(username='bobi1', password='bobi123')

    def test_biotics_user_details_view_template_used(self):
        response = self.client.get(self.details_url)
        self.assertTemplateUsed(response, 'profiles/profile-details.html')
        self.assertEqual(response.status_code, 200)

    def test_biotics_user_details_view_context(self):
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user, self.other_user)

        response = self.client.get(self.details_url)
        self.assertEqual(response.context['object'], self.other_user)
        self.assertTrue('total_publications' in response.context)
        self.assertTrue('other_users' in response.context)
        self.assertTrue('other_user' in response.context)
        self.assertTrue('paid_trainings' in response.context)
        self.assertTrue('followers_count' in response.context)
        self.assertTrue('following_count' in response.context)


class BioticsUserEditViewTest(TestCase):
    def setUp(self):
        self.user = BioticsUserModel\
            .objects.create_user(username='bobi111', email='bobi1@example.com', password='bobi123')
        self.biotics_user = BioticsUserModel.objects.create(username='bobi112', email='bobi12@example.com')
        self.edit_url = reverse('edit_profile', args=[self.biotics_user.pk])
        self.client.login(username='bobi111', password='bobi123')
        self.form_data = {
            'username': 'newusername',
            'first_name': 'Gosho',
            'last_name': 'Sedev',
            'email': 'newemail@example.com',
        }

    def test_biotics_user_edit_view_template_used(self):
        response = self.client.get(self.edit_url)
        self.assertTemplateUsed(response, 'profiles/profile-edit.html')
        self.assertEqual(response.status_code, 200)

    def test_biotics_user_edit_view_valid_form(self):
        response = self.client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, reverse('profile_details', kwargs={
            'pk': self.biotics_user.pk}))  # Redirects after successful form submission
        self.biotics_user.refresh_from_db()
        self.assertEqual(self.biotics_user.username, 'newusername')
        self.assertEqual(self.biotics_user.first_name, 'Gosho')
        self.assertEqual(self.biotics_user.last_name, 'Sedev')
        self.assertEqual(self.biotics_user.email, 'newemail@example.com')
        # Add assertions for other form fields

    def test_biotics_user_edit_view_invalid_form(self):
        invalid_form_data = {
            'email': 'invalidemail',  # Invalid email format
        }
        response = self.client.post(self.edit_url, data=invalid_form_data)
        self.assertEqual(response.status_code, 200)

