from django.test import TestCase
from django.urls import reverse
from ...services import animal_services
from django.contrib.auth.models import User


class AnimalViewsTestCast(TestCase):
    def setUp(self):
        self.form_data = {
            "name": "Test Animal",
            "scientificName": "Test Animal",
            "habitat": "Test Habitat",
            "diet": "Test Diet",
            "behaviour": "Test Behaviour",
            "weightMale": "100",
            "weightFemale": "120",
            "image": "Test Image",
            "conservationStatus": "Test Conservation Status",
            "funFacts": "Test Fun Facts"
        }
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.url1 = reverse("animals")

    def test_all_animals_view_not_logged_in(self):
        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login") + "?next=/animals/")

        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login") + "?next=/animals/")

        response = self.client.post(self.url1, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/animals/")

        response = self.client.post(self.url1, {
            "name": "Test Animal",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/animals/")

    def test_all_animals_view_get_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.get(self.url1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_animals.html")
        self.assertIn("animals", response.context)
        self.assertIn("form", response.context)

    def test_all_animals_view_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(self.url1, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_animals.html")
        self.assertIn("animals", response.context)
        self.assertIn("form", response.context)

    def test_all_animals_view_with_valid_form_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        count = len(animal_services.get_animals_list())
        response = self.client.post(self.url1, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_animals.html")
        self.assertEqual(len(animal_services.get_animals_list()), count + 1)
        self.assertIn("Animal created successfully", [
                      m.message for m in response.context['messages']])

    def test_all_animals_view_with_invalid_form_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(self.url1, {
            "name": "Test Animal",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_animals.html")
        self.assertIn("Animal not created, check formatting", [
            m.message for m in response.context['messages']])

    def test_remove_animal_view_not_logged_in(self):
        response = self.client.post(
            reverse("remove_animal", args=["1"]), follow=True)
        self.assertRedirects(response, reverse("login") + "?next=/animals/")
