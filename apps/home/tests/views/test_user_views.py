from django.test import TestCase
from django.urls import reverse
from ...views import user_views


class UserViewsTestCast(TestCase):
    def test_all_users_view_not_logged_in(self):
        response = self.client.get(reverse("users"))
        self.assertEqual(response.status_code, 302)
