from django.test import TestCase
from ....views.extras import miscellaneous_views_extras


class MiscellaneousViewsExtrasTestCase(TestCase):
    def test_set_list_to_length(self, lst=[1, 2, 3], length=5):
        result = miscellaneous_views_extras.set_list_to_length(lst, length)
        self.assertEqual(result, [1, 2, 3, 0, 0])
