from django.test import TestCase

from .forms import TrainingCreateForm
from .models import TrainingModel


class TrainingModelTest(TestCase):
    def test_create_training_model(self):
        training = TrainingModel.objects.create(
            title='Test Training',
            description='This is a test training.',
            price=500,
            type_of_training='Botany'
        )

        self.assertEqual(training.title, 'Test Training')
        self.assertEqual(training.description, 'This is a test training.')
        self.assertEqual(training.price, 500)
        self.assertEqual(training.type_of_training, 'Botany')

    def test_training_model_str(self):
        training = TrainingModel.objects.create(
            title='Test Training',
            description='This is a test training.',
            price=500,
            type_of_training='Botany'
        )

        self.assertEqual(str(training), 'Test Training')


class TrainingCreateFormTest(TestCase):

    def test_invalid_form(self):
        form_data = {

        }
        form = TrainingCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_date_format(self):
        form_data = {
            'title': 'Test Training',
            'description': 'This is a test training.',
            'price': 490,
            'date_of_training': '08/15/2023',
            'type_of_training': 'Botany',
        }
        form = TrainingCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
