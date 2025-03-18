from django.test import TestCase
from django.urls import reverse
from ...services import animal_services
from django.contrib.auth.models import User
from ...services.services_extras import *


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
        self.animals_url = reverse("animals")
        self.remove_animal_url = reverse("remove_animal", args=["1"])
        self.edit_animal_url = reverse("edit_animal", args=["1"])

    def tearDown(self):
        super().tearDown()
        animals = animal_services.get_animals_list()
        test_animal = next(
            (animal for animal in animals if animal["name"] == "Test Animal"), None)
        if test_animal:
            animal_services.remove_animal(test_animal["id"])

    def test_all_animals_view_not_logged_in_get(self):
        response = self.client.get(self.animals_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login") + "?next=/animals/")

    def test_all_animals_view_not_logged_in_post_valid_form(self):
        response = self.client.post(
            self.animals_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/animals/")

    def test_all_animals_view_not_logged_in_post_invalid_form(self):
        response = self.client.post(self.animals_url, {
            "name": "Test Animal",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/animals/")

    def test_all_animals_view_get_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.get(self.animals_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_animals.html")
        self.assertIn("animals", response.context)
        self.assertIn("form", response.context)

    def test_all_animals_view_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(
            self.animals_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_animals.html")
        self.assertIn("animals", response.context)
        self.assertIn("form", response.context)

    def test_all_animals_view_with_valid_form_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        count = len(animal_services.get_animals_list())
        response = self.client.post(
            self.animals_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_animals.html")
        self.assertEqual(len(animal_services.get_animals_list()), count + 1)
        self.assertIn("Animal created successfully", [
                      m.message for m in response.context['messages']])
        self.assertIn("animals", response.context)
        self.assertIn("form", response.context)

    def test_all_animals_view_with_invalid_form_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(self.animals_url, {
            "name": "Test Animal",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_animals.html")
        self.assertIn("Animal not created, check formatting", [
            m.message for m in response.context['messages']])
        self.assertIn("animals", response.context)
        self.assertIn("form", response.context)

    def test_remove_animal_view_not_logged_in_get(self):
        response = self.client.get(self.remove_animal_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/animals/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_remove_animal_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(self.remove_animal_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("animals"))
        self.assertIn("Animal removed successfully", [
                      m.message for m in response.context['messages']])

    def test_edit_animal_not_logged_in_get(self):
        add_animal = f"""
            mutation createAnimal {{
                createAnimal(input: {{
                    id: "1",
                    name: "Test Animal",
                    scientificName: "Test Animal"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_animal)

        response = self.client.get(self.edit_animal_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/animals/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_edit_animal_not_logged_in_post_valid_form(self):
        add_animal = f"""
            mutation createAnimal {{
                createAnimal(input: {{
                    id: "1",
                    name: "Test Animal",
                    scientificName: "Test Animal"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_animal)

        response = self.client.post(
            self.edit_animal_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/animals/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_edit_animal_not_logged_in_post_invalid_form(self):
        add_animal = f"""
            mutation createAnimal {{
                createAnimal(input: {{
                    id: "1",
                    name: "Test Animal",
                    scientificName: "Test Animal"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_animal)

        response = self.client.post(self.edit_animal_url, {
            "name": "Test Animal",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/animals/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_edit_animal_get_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        add_animal = f"""
            mutation createAnimal {{
                createAnimal(input: {{ 
                    id: "1",
                    name: "Test Animal",
                    scientificName: "Test Animal"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_animal)

        response = self.client.get(self.edit_animal_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/edit_animal.html")
        self.assertIn("form", response.context)

    def test_edit_animal_with_valid_form_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        add_animal = f"""
            mutation createAnimal {{
                createAnimal(input: {{ 
                    id: "1",
                    name: "Test Animal",
                    scientificName: "Test Animal"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_animal)

        response = self.client.post(
            self.edit_animal_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_animals.html")
        messages = [m.message for m in response.context['messages']]
        self.assertTrue(
            any('"Test Animal" edited successfully' in message for message in messages))

    def test_edit_animal_with_invalid_form_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        add_animal = f"""
            mutation createAnimal {{
                createAnimal(input: {{ 
                    id: "1",
                    name: "Test Animal",
                    scientificName: "Test Animal"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_animal)

        response = self.client.post(self.edit_animal_url, {
            "name": 12345,
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/edit_animal.html")
        self.assertIn("animal", response.context)
        self.assertIn("form", response.context)
        messages = [m.message for m in response.context['messages']]
        self.assertFalse(
            any('"Test Animal" edited successfully' in message for message in messages))
