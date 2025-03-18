from django.test import TestCase
from django.urls import reverse
from ...views import user_views


class UserViewsTestCast(TestCase):
    def test_all_users_view_not_logged_in(self):
        response = self.client.get(reverse("users"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login") + "?next=/users/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_all_users_view_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.get(reverse("users"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_users.html")
        self.assertIn("users", response.context)
        self.assertIn("isFirstPage", response.context)
