from django.test import TestCase
from django.urls import reverse
from ...views import event_views


class EventViewsTestCast(TestCase):
    def setUp(self):
        self.url = reverse("events")

    def test_all_events_view_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    # def test_delete_event_view(self):
    #     response = self.client.get(reverse("delete_event", args=["1"]))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse("all_events"))

    # def test_add_place_to_event_view(self):
    #     response = self.client.get(
    #         reverse("add_place_to_event", args=["1", "1"]))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse("all_events"))

    # def test_edit_event_view(self):
    #     response = self.client.get(reverse("edit_event", args=["1"]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "home/edit_event.html")

    # def test_remove_place_from_event_view(self):
    #     response = self.client.get(
    #         reverse("remove_place_from_event", args=["1", "1"]))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse("all_events"))
