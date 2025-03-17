from django.test import TestCase
from django.urls import reverse
from ...views import miscellaneous_views


class MiscellaneousViewsTestCast(TestCase):
    def test_statistics_view_not_logged_in(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
