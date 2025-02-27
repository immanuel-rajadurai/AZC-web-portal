from django.test import TestCase
import json

from ...services import event_tag_services

from ...services.services_extras import *

class EventTagServices(TestCase):
    def delete_test_tag(self):
        tags = event_tag_services.get_tags('test event_id')
        tag = next((tag for tag in tags if tag['tagName'] == 'test tagName'), None)
        event_tag_services.delete_tag('test event_id', tag['tagName']) if tag else None

    def setUp(self):
        event_tag_services.create_tag('test event_id', 'test tagName')

    def tearDown(self):
        super().tearDown()
        self.delete_test_tag()

    def get_test_tag(self):
        tags = event_tag_services.get_tags('test event_id') 
        return next((tag for tag in tags if tag['tagName'] == 'test tagName'), None)

    def test_get_tags(self):
        tags = event_tag_services.get_tags('test event_id')
        self.assertNotEqual(tags, [])

    def test_create_tag(self):
        tag = self.get_test_tag()
        self.assertIsNotNone(tag)
        self.assertEqual(tag['tagName'], 'test tagName')

    def test_delete_tag(self):
        tag = self.get_test_tag()
        self.assertIsNotNone(tag)

        event_tag_services.delete_tag('test event_id', tag['tagName'])

        tags = event_tag_services.get_tags('test event_id')
        tag2 = next((tag for tag in tags if tag['tagName'] == 'test tagName'), None)
        self.assertIsNone(tag2)