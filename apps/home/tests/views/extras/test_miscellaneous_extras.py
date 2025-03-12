from django.test import TestCase
from ....views.extras import miscellaneous_extras


class MiscellaneousExtrasTestCase(TestCase):
    def test_split_tags(self, tags="one, two, three"):
        result = miscellaneous_extras.split_tags(tags)
        self.assertEqual(result, ["one", "two", "three"])
