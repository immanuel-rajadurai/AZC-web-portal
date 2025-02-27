from django.test import TestCase
import json

from ...services import event_tag_services

from ...services.services_extras import *

class EventTagServices(TestCase):
    def delete_tag(self):
        tags = event_tag_services.get_tags('TEST')
        tag = next((tag for tag in tags if tag['tagName'] == 'TEST'), None)
        event_tag_services.delete_tag('TEST', tag['tagName']) if tag else None

    def setUp(self):
        self.delete_tag()

    def tearDown(self):
        super().tearDown()
        self.delete_tag()

        # print(event_tag_services.get_tags('TEST'))

    def test_get_tags(self):
        event_tag_services.create_tag('TEST', 'TEST')
        tags = event_tag_services.get_tags('TEST')
        self.assertNotEqual(tags, [])

    def test_create_tag(self):
        event_tag_services.create_tag('TEST', 'TEST')

        tags = event_tag_services.get_tags('TEST')
        tag = next((tag for tag in tags if tag['tagName'] == 'TEST'), None)
        self.assertIsNotNone(tag)

        self.assertEqual(tag['tagName'], 'TEST')

    def test_delete_tag(self):
        event_tag_services.create_tag('TEST', 'TEST')
        tags = event_tag_services.get_tags('TEST')
        tag = next((tag for tag in tags if tag['tagName'] == 'TEST'), None)
        self.assertIsNotNone(tag)

        event_tag_services.delete_tag('TEST', tag['tagName'])
        tags = event_tag_services.get_tags('TEST')
        tag = next((tag for tag in tags if tag['tagName'] == 'TEST'), None)
        self.assertIsNone(tag)