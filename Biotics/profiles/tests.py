from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import BioticsUserModel


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

    def test_get_user_name(self):
        self.assertEqual(self.user.get_user_name(), 'bobi kamenov')

        self.user.last_name = ''
        self.assertEqual(self.user.get_user_name(), 'bobi')

        self.user.first_name = ''
        self.user.last_name = 'kamenov'
        self.assertEqual(self.user.get_user_name(), 'kamenov')

        self.user.first_name = ''
        self.user.last_name = ''
        self.assertEqual(self.user.get_user_name(), 'bobi123')

    def test_total_followers(self):
        self.assertEqual(self.user.total_followers, 0)

        follower = BioticsUserModel.objects.create_user(username='follower', email='follower@example.com')
        self.user.followers.add(follower)
        self.assertEqual(self.user.total_followers, 1)

    def test_get_following_count(self):
        self.assertEqual(self.user.get_following_count, 0)

        following_user = BioticsUserModel.objects.create_user(username='following', email='following@example.com')
        self.user.following.add(following_user)
        self.assertEqual(self.user.get_following_count, 1)

    def test_total_followers_count(self):
        follower = BioticsUserModel.objects.create_user(username='follower', email='follower@example.com')
        self.user.followers.add(follower)
        self.assertEqual(self.user.total_followers, 1)

        for i in range(5):
            follower = BioticsUserModel.objects.create_user(username=f'follower{i}', email=f'follower{i}@example.com')
            self.user.followers.add(follower)
        self.assertEqual(self.user.total_followers, 6)

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

    def test_user_name_property_default(self):
        default_user = BioticsUserModel.objects.create_user(username='defaultuser', email='default@example.com')
        self.assertEqual(default_user.get_user_name(), 'defaultuser')

    def test_user_name_property_username_only(self):
        username_only_user = BioticsUserModel.objects.create_user(username='usernameonly', email='username@example.com')
        self.assertEqual(username_only_user.get_user_name(), 'usernameonly')

    def test_user_name_property_full_name(self):
        self.user.first_name = 'bobi'
        self.user.last_name = 'kamenov'
        self.assertEqual(self.user.get_user_name(), 'bobi kamenov')

    def test_user_age_validator(self):
        self.user.age = 30
        self.user.full_clean()

        with self.assertRaises(ValidationError):
            self.user.age = 17
            self.user.full_clean()

        self.user.age = 18
        self.user.full_clean()
