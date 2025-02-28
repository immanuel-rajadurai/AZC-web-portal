from django.test import TestCase
from ...services import event_services

class EventServicesTestCase(TestCase):
    def delete_test_event(self):
        events = event_services.get_events_list()
        event = next((event for event in events if event['name'] == 'TEST'), None)
        event_services.delete_event(event['id']) if event else None

    def setUp(self):
        event_services.create_event('TEST', 'testing description', 'https://www.google.com')

    def tearDown(self):
        super().tearDown()
        self.delete_test_event()

    def get_test_event(self):
        events = event_services.get_events_list()
        return next((event for event in events if event['name'] == 'TEST'), None)

    def test_get_events_list(self):
        events = event_services.get_events_list()
        self.assertNotEqual(events, [])

    def test_create_event(self):        
        event = self.get_test_event()

        self.assertIsNotNone(event)
        self.assertEqual(event['name'], 'TEST')
        self.assertEqual(event['description'], 'testing description')
        self.assertEqual(event['image'], 'https://www.google.com')

    def test_delete_event(self):        
        event = self.get_test_event()
        id = event['id']
        self.assertIsNotNone(event)

        event_services.delete_event(event['id'])

        event2 = self.get_test_event()
        self.assertIsNone(event2)

        attached_relationships = event_services.get_attached_relationships(id)
        self.assertEqual(attached_relationships, [])

    def test_edit_event(self):
        event = self.get_test_event()
        self.assertIsNotNone(event)
        self.assertEqual(event['name'], 'TEST')
        self.assertEqual(event['description'], 'testing description')
        self.assertEqual(event['image'], 'https://www.google.com')

        event_services.edit_event(event['id'], 'TEST2', 'testing description2', 'https://www.google2.com')
        event2 = event_services.get_event(event['id'])

        self.assertEqual(event2['name'], 'TEST2')
        self.assertEqual(event2['description'], 'testing description2')
        self.assertEqual(event2['image'], 'https://www.google2.com')

    def test_get_event(self):
        event = self.get_test_event()
        self.assertIsNotNone(event)
        self.assertEqual(event['name'], 'TEST')
        self.assertEqual(event['description'], 'testing description')
        self.assertEqual(event['image'], 'https://www.google.com')
