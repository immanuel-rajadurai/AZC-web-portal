from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ...services import place_services, animal_services
from ...services.services_extras import sendAWSQuery


class PlaceViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')
        self.place_url = reverse("places")
        self.delete_place_url = reverse("delete_place", args=["1"])
        self.edit_place_url = reverse("edit_place", args=["1"])
        self.add_animal_to_place_url = reverse(
            "add_animal_to_place", args=["1", "1"])
        self.remove_animal_from_place_url = reverse(
            "remove_animal_from_place", args=["1", "1"])
        self.form_data = {
            "name": "Test Place",
            "description": "Test Description",
            "isOpen": True,
            "image": "Test Image"
        }

    def tearDown(self):
        super().tearDown()
        places = place_services.get_places_list()
        test_place = next(
            (place for place in places if place["name"] == "Test Place"), None)
        if test_place:
            place_services.delete_place(test_place["id"])

        test_animal = next(
            (animal for animal in animal_services.get_animals_list() if animal["name"] == "Test Animal"), None)
        if test_animal:
            animal_services.delete_animal(test_animal["id"])

    def test_all_places_view_not_logged_in_get(self):
        response = self.client.get(reverse("places"), follow=True)
        self.assertRedirects(response, reverse("login") + "?next=/places/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_all_places_view_not_logged_in_post_valid_form(self):
        response = self.client.post(
            self.place_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/places/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_all_places_view_not_logged_in_post_invalid_form(self):
        response = self.client.post(self.place_url, {
            "name": "Test Place",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/places/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_all_places_view_get_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.get(self.place_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_places.html")
        self.assertIn("places", response.context)
        self.assertIn("linked_animals", response.context)
        self.assertIn("form", response.context)

    def test_all_places_view_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(
            self.place_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_places.html")
        self.assertIn("places", response.context)
        self.assertIn("linked_animals", response.context)
        self.assertIn("form", response.context)

    def test_all_places_view_with_valid_form_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        count = len(place_services.get_places_list())
        response = self.client.post(
            self.place_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_places.html")
        self.assertEqual(len(place_services.get_places_list()), count + 1)
        self.assertIn("Place created successfully", [
                      m.message for m in response.context['messages']])
        self.assertIn("places", response.context)
        self.assertIn("linked_animals", response.context)
        self.assertIn("form", response.context)

    def test_all_places_view_with_invalid_form_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(
            self.place_url, {
                "name": "Test Place",
            }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_places.html")
        self.assertIn("places", response.context)
        self.assertIn("linked_animals", response.context)
        self.assertIn("form", response.context)
        self.assertIn("Place not created, check formatting", [
                      m.message for m in response.context['messages']])

    def test_delete_place_view_not_logged_in_get(self):
        response = self.client.get(self.delete_place_url, follow=True)
        self.assertRedirects(response, reverse("login") + "?next=/places/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_delete_place_view_not_logged_in_post(self):
        response = self.client.post(self.delete_place_url, follow=True)
        self.assertRedirects(response, reverse("login") + "?next=/places/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_delete_place_view_logged_in_get(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.get(self.delete_place_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("places"))
        self.assertIn("Place deleted successfully", [
                      m.message for m in response.context['messages']])

    def test_delete_place_view_logged_in_post(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(self.delete_place_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("places"))
        self.assertIn("Place deleted successfully", [
                      m.message for m in response.context['messages']])

    def test_add_animal_to_place_view_not_logged_in_get(self):
        response = self.client.get(self.add_animal_to_place_url, follow=True)
        self.assertRedirects(response, reverse("login") + "?next=/places/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_add_animal_to_place_view_not_logged_in_post(self):
        response = self.client.post(self.add_animal_to_place_url, follow=True)
        self.assertRedirects(response, reverse("login") + "?next=/places/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_add_animal_to_place_view_logged_in_get(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.get(self.add_animal_to_place_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("places"))
        self.assertIn("Animal assigned successfully", [
                      m.message for m in response.context['messages']])

    def test_add_animal_to_place_view_logged_in_post(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(self.add_animal_to_place_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("places"))
        self.assertIn("Animal assigned successfully", [
                      m.message for m in response.context['messages']])

    def test_remove_animal_from_place_view_not_logged_in_get(self):
        response = self.client.get(
            self.remove_animal_from_place_url, follow=True)
        self.assertRedirects(response, reverse("login") + "?next=/places/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_remove_animal_from_place_view_not_logged_in_post(self):
        response = self.client.post(
            self.remove_animal_from_place_url, follow=True)
        self.assertRedirects(response, reverse("login") + "?next=/places/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_remove_animal_from_place_view_logged_in_get(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.get(
            self.remove_animal_from_place_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("places"))
        self.assertIn("Animal detached successfully", [
                      m.message for m in response.context['messages']])

    def test_remove_animal_from_place_view_logged_in_post(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(
            self.remove_animal_from_place_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("places"))
        self.assertIn("Animal detached successfully", [
                      m.message for m in response.context['messages']])

    def test_edit_place_view_not_logged_in_get(self):
        add_place = f"""
            mutation createPlace {{
                createPlace(input: {{
                    id: "1",
                    name: "Test Place",
                    description: "Test Description",
                    isOpen: true,
                    image: "Test Image"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_place)

        response = self.client.get(self.edit_place_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/places/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_edit_place_view_not_logged_in_post_valid_form(self):
        add_place = f"""
            mutation createPlace {{
                createPlace(input: {{
                    id: "1",
                    name: "Test Place",
                    description: "Test Description",
                    isOpen: true,
                    image: "Test Image"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_place)

        response = self.client.post(
            self.edit_place_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/places/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_edit_place_view_not_logged_in_post_invalid_form(self):
        add_place = f"""
            mutation createPlace {{
                createPlace(input: {{
                    id: "1",
                    name: "Test Place",
                    description: "Test Description",
                    isOpen: true,
                    image: "Test Image"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_place)

        response = self.client.post(
            self.edit_place_url, {
                "name": "Test Place",
            }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/places/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_edit_place_view_get_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        add_place = f"""
            mutation createPlace {{
                createPlace(input: {{
                    id: "1",
                    name: "Test Place",
                    description: "Test Description",
                    isOpen: true,
                    image: "Test Image"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_place)

        response = self.client.get(self.edit_place_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/edit_place.html")
        self.assertIn("form", response.context)
