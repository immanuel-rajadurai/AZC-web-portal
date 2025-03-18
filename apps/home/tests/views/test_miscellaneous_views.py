from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class MiscellaneousViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')
        self.statistics_url = reverse("home")

    def test_statistics_view_not_logged_in(self):
        response = self.client.get(self.statistics_url, follow=True)
        self.assertRedirects(response, reverse("login") + "?next=/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_statistics_view_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.get(reverse("home"), follow=True)
        self.assertTemplateUsed(response, "home/statistics.html")
        self.assertIn("segment", response.context)
        self.assertIn("numberOfVisitors", response.context)
        self.assertIn("animalChallengeCompletions", response.context)
