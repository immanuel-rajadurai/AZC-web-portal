from django.test import TestCase
from ...services import tag_services

from ...services.services_extras import sendAWSQuery


class TagServicesTestCase(TestCase):
    def create_tag(self, name):
        create_tag = f"""
            mutation createTag {{
                createTag(input: {{ name: "{name}" }}) {{
                    name
                }}
            }}
        """

        sendAWSQuery(create_tag)

    def delete_tag(self, name):
        tags = tag_services.get_tags_list()
        tag = next((tag for tag in tags if tag["name"] == name), None)
        delete_tag = f"""
            mutation deleteTag {{
                deleteTag(input: {{ name: "{tag['name']}" }}) {{
                    name
                }}
            }}
        """

        sendAWSQuery(delete_tag)

    def setUp(self):
        self.create_tag("test_tag")

    def tearDown(self):
        super().tearDown()
        self.delete_tag("test_tag")

    def test_get_tags_list(self):
        tags = tag_services.get_tags_list()
        self.assertNotEqual(tags, [])
