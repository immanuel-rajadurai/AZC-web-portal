from django.test import TestCase

from ...templatetags import place_extras
from ...services import place_services


class PlaceExtrasTestCase(TestCase):
    def delete_test_place(self):
        places = place_services.get_places_list()
        place = next((place for place in places if place['name'] == 'TEST'), None)
        place_services.delete_place(place['id']) if place else None

    def get_test_place(self):
        places = place_services.get_places_list()
        return next((place for place in places if place['name'] == 'TEST'), None)
    
    def setUp(self):
        place_services.create_place('TEST', 'testing description', 'https://www.google.com')

    def tearDown(self):
        super().tearDown()
        self.delete_test_place()

    def test_get_place_name(self):
        place = self.get_test_place()
        self.assertIsNotNone(place)

        self.assertEqual(place_extras.get_place_name(place['id']), 'TEST')

    def test_get_place_name_undefined(self):
        self.assertEqual(place_extras.get_place_name(1234), 'Undefined')