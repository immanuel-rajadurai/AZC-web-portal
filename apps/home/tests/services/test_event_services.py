from django.test import TestCase
import json

from ...services import event_services

from ...services.services_extras import *

class EventServicesTestCase(TestCase):
    def delete_event(self):
        events = event_services.get_events_list()
        event = next((event for event in events if event['name'] == 'TEST'), None)
        event_services.delete_event(event['id']) if event else None

    def setUp(self):
        self.delete_event()

    def tearDown(self):
        super().tearDown()
        self.delete_event()

        # print(event_services.get_events_list())

    def test_get_events_list(self):
        event_services.create_event('TEST', 'testing description', 'https://www.google.com')
        events = event_services.get_events_list()
        self.assertNotEqual(events, [])

    def test_create_event(self):
        event_services.create_event('TEST', 'testing description', 'https://www.google.com')
        
        events = event_services.get_events_list()
        event = next((event for event in events if event['name'] == 'TEST'), None)

        self.assertIsNotNone(event)
        self.assertEqual(event['name'], 'TEST')
        self.assertEqual(event['description'], 'testing description')
        self.assertEqual(event['image'], 'https://www.google.com')

    def test_delete_event(self):
        event_services.create_event('TEST', 'testing description', 'https://www.google.com')
        
        events = event_services.get_events_list()
        event = next((event for event in events if event['name'] == 'TEST'), None)
        id = event['id']
        self.assertIsNotNone(event)

        event_services.delete_event(event['id'])

        events = event_services.get_events_list()
        event = next((event for event in events if event['name'] == 'TEST'), None)
        self.assertIsNone(event)

        attached_relationships = event_services.get_attached_relationships(id)
        self.assertEqual(attached_relationships, [])

    def test_edit_event(self):
        event_services.create_event('TEST', 'testing description', 'https://www.google.com')

        events = event_services.get_events_list()
        event = next((event for event in events if event['name'] == 'TEST'), None)
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
        event_services.create_event('TEST', 'testing description', 'https://www.google.com')

        events = event_services.get_events_list()
        event = next((event for event in events if event['name'] == 'TEST'), None)

        event2 = event_services.get_event(event['id'])
        self.assertEqual(event2['name'], 'TEST')
        self.assertEqual(event2['description'], 'testing description')
        self.assertEqual(event2['image'], 'https://www.google.com')
