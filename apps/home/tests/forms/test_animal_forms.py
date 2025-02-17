from unittest import TestCase
from ...forms.animal_forms import AnimalForm

class AnimalFormTestCase(TestCase):
    def test_form_valid_data_without_not_required_fields(self):
        form = AnimalForm(data={
            'name': 'test',
            'scientificName': 'test'
        })
        self.assertTrue(form.is_valid())
        
    def test_form_valid_data_with_all_fields(self):
        form = AnimalForm(data={
            'name': 'test',
            'scientificName': 'test',
            'habitat': 'test',
            'diet': 'test',
            'behaviour': 'test',
            'weightMale': 'test',
            'weightFemale': 'test',
            'image': 'test',
            'conservationStatus': 'test',
            'funFacts': 'test'
        })
        self.assertTrue(form.is_valid())
        
    def test_form_invalid_data(self):
        form = AnimalForm(data={
            'name': '',
            'scientificName': '',
        })
        
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['scientificName'], ['This field is required.'])