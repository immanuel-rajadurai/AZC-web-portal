from django.test import TestCase
import json

from ...services import place_event_services, place_services, animal_services

from ...services.services_extras import *

class PlaceEventServicesTestCase(TestCase):
    def delete_place_event(self):
        places = place_services.get_places_list()
        place = next((place for place in places if place['name'] == 'TEST'), None)
        place_services.delete_place(place['id']) if place else None

        events = place_event_services.get_events_list()
        event = next((event for event in events if event['name'] == 'TEST'), None)
        place_event_services.delete_event(event['id']) if event else None

    def setUp(self):
        self.delete_place_event()
        place_services.create_place('TEST', 'testing place', True, 'https://www.google.com')
        place_event_services.create_event('TEST', 'testing description', 'testing date', 'https://www.google.com')

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        cls().delete_place_event()
        # print(place_services.get_places_list())
        # print(event_services.get_events_list())