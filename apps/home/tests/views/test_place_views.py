from django.test import TestCase
from django.urls import reverse
from ...views import place_views


class PlaceViewsTestCast(TestCase):
    def test_all_places_view_not_logged_in(self):
        response = self.client.get(reverse("places"))
        self.assertEqual(response.status_code, 302)
