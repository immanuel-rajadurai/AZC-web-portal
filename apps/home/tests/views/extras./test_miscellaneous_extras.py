from django.test import TestCase
from ....views.extras import miscellaneous_extras


class MiscellaneousExtrasTestCase(TestCase):
    def test_get_id_from_filter(self):
        data = [
            {"id": 1},
            {"id": 2},
            {"id": 3},
        ]

        result = miscellaneous_extras.get_ids_from_filter(data, "id")
        self.assertEqual(result, [1, 2, 3])

    def test_split_tags(self, tags="one, two, three"):
        result = miscellaneous_extras.split_tags(tags)
        self.assertEqual(result, ["one", "two", "three"])
