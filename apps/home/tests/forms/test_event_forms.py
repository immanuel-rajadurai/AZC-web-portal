from django.test import TestCase
from ...forms.event_forms import EventForm

class EventFormTestCase(TestCase):
    def test_form_valid_data_without_not_required_fields(self):
        form = EventForm(data={
            'name': 'test',
            'description': 'test'
        })
        self.assertTrue(form.is_valid())
        
    def test_form_valid_with_all_fields(self):
        form = EventForm(data={
            'name': 'test',
            'description': 'test',
            'image': 'test',
            'tags': 'test'
        })
        self.assertTrue(form.is_valid())
        
    def test_form_invalid_data(self):
        form = EventForm(data={
            'name': '',
            'description': '',
        })
        
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['description'], ['This field is required.'])