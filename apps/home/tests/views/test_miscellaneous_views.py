from django.test import TestCase
from django.urls import reverse
from ...views import miscellaneous_views


class MiscellaneousViewsTestCast(TestCase):
    def test_statistics_view_not_logged_in(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login") + "?next=/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_statistics_view_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/statistics.html")
