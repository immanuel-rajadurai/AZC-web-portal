from django.test import TestCase

from ...templatetags import miscellaneous_extras


class MiscellaneousExtrasTestCase(TestCase):
    def setUp(self):
        pass

    def test_get_item(self):
        self.assertEqual(
            miscellaneous_extras.get_item({"key": "value"}, "key"), "value"
        )
