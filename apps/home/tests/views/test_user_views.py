from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')
        self.users_url = reverse("users")

    def test_all_users_view_not_logged_in(self):
        response = self.client.get(reverse("users"), follow=True)
        self.assertRedirects(response, reverse("login") + "?next=/users/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_all_users_view_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.get(reverse("users"), follow=True)
        self.assertTemplateUsed(response, "home/show_users.html")
        self.assertIn("users", response.context)
        self.assertIn("isFirstPage", response.context)
