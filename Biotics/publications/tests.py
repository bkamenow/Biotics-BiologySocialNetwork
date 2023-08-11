from django.test import TestCase, Client
from django.urls import reverse

from django.test import RequestFactory

from Biotics.profiles.models import BioticsUserModel
from Biotics.publications.models import PublicationModel
from Biotics.publications.views import PublicationListView


class PublicationModelTest(TestCase):
    def setUp(self):
        self.user = BioticsUserModel.objects.create_user(
            username='bobi111',
            email='bobi1@example.com',
            password='bobi123'
        )
        self.publication = PublicationModel.objects.create(
            title='Test Publication',
            description='This is a test publication.',
            type_of_publication='Botany',
            user=self.user
        )

    def test_user_has_liked(self):
        self.assertFalse(self.publication.user_has_liked(self.user))

        # Let's assume 'user' has liked the publication
        self.publication.like_set.create(user=self.user)
        self.assertTrue(self.publication.user_has_liked(self.user))

    def test_likes_count_default_value(self):
        self.assertEqual(self.publication.likes_count, 0)

    def test_publication_creation(self):
        publication = PublicationModel.objects.create(
            title='Another Publication',
            description='This is another test publication.',
            type_of_publication='Microbiology',
            user=self.user
        )
        self.assertEqual(publication.title, 'Another Publication')
        self.assertEqual(publication.description, 'This is another test publication.')
        self.assertEqual(publication.type_of_publication, 'Microbiology')
        self.assertEqual(publication.user, self.user)
        self.assertEqual(publication.likes_count, 0)


class PublicationListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = BioticsUserModel.objects.create_user(username='bobi1', email='bobi1@example.com', password='bobi123')
        self.publication = PublicationModel.objects.create(title='TestPublication', user=self.user)
        self.list_url = reverse('publications')
        self.client = Client()
        self.client.login(username='bobi1', password='bobi123')

    def test_publication_list_view_template_used(self):
        request = self.factory.get(self.list_url)
        request.user = self.user
        response = PublicationListView.as_view()(request)

        expected_template = 'publications/publications.html'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], expected_template)

    def test_publication_list_view_context(self):
        request = self.factory.get(self.list_url)
        request.user = self.user
        response = PublicationListView.as_view()(request)
        self.assertEqual(list(response.context_data['all_publications']), [self.publication])
        self.assertTrue('form' in response.context_data)

    def test_publication_list_view_pagination(self):
        for i in range(15):
            PublicationModel.objects.create(title=f'Test Publication {i}', user=self.user)

        request = self.factory.get(self.list_url)
        request.user = self.user
        response = PublicationListView.as_view()(request)
        self.assertEqual(len(response.context_data['all_publications']), 10)

        request = self.factory.get(self.list_url, {'page': 2})
        request.user = self.user
        response = PublicationListView.as_view()(request)
        self.assertEqual(len(response.context_data['all_publications']), 6)
