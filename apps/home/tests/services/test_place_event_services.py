from django.test import TestCase
from ...services import place_event_services, place_services, event_services


class PlaceEventServicesTestCase(TestCase):
    def delete_test_place_event(self):
        places = place_services.get_places_list()
        place = next((place for place in places if place['name'] == 'TEST'), None)
        place_services.delete_place(place['id']) if place else None

        events = event_services.get_events_list()
        event = next((event for event in events if event['name'] == 'TEST'), None)
        event_services.delete_event(event['id']) if event else None

    def setUp(self):
        place_services.create_place('TEST', 'testing description', True, 'https://www.google.com')
        event_services.create_event('TEST', 'testing description', 'https://www.google.com')

    def tearDown(self):
        super().tearDown()
        self.delete_test_place_event()

    def get_test_place(self):
        places = place_services.get_places_list()
        return next((place for place in places if place['name'] == 'TEST'), None)
    
    def get_test_event(self):
        events = event_services.get_events_list()
        return next((event for event in events if event['name'] == 'TEST'), None)
    
    def test_get_testing_place(self):
        place = self.get_test_place()

        place = place_services.get_place(place['id'])
        self.assertEqual(place['name'], 'TEST')
        self.assertEqual(place['description'], 'testing description')
        self.assertEqual(place['isOpen'], True)
        self.assertEqual(place['image'], 'https://www.google.com')

    def test_gest_testing_event(self):
        event = self.get_test_event()

        event = event_services.get_event(event['id'])
        self.assertEqual(event['name'], 'TEST')
        self.assertEqual(event['description'], 'testing description')
        self.assertEqual(event['image'], 'https://www.google.com')

    def test_get_places_linked_to_event(self):
        event = self.get_test_event()
        places = place_event_services.get_places_linked_to_event(event['id'])
        self.assertEqual(places, [])

    def test_add_place_to_event(self):
        place = self.get_test_place()
        event = self.get_test_event()
        self.assertIsNotNone(place)
        self.assertIsNotNone(event)

        place_event_services.add_place_to_event(place['id'], event['id'])
        places = place_event_services.get_places_linked_to_event(event['id'])
        self.assertEqual(places, [{'placeID': place['id']}])

    def test_remove_place_from_event(self):
        place = self.get_test_place()
        event = self.get_test_event()
        self.assertIsNotNone(place)
        self.assertIsNotNone(event)

        place_event_services.add_place_to_event(place['id'], event['id'])
        places = place_event_services.get_places_linked_to_event(event['id'])
        self.assertEqual(places, [{'placeID': place['id']}])
        
        place_event_services.remove_place_from_event(place['id'], event['id'])
        places = place_event_services.get_places_linked_to_event(event['id'])
        self.assertEqual(places, [])