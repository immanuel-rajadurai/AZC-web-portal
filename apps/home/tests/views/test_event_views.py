from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ...services.services_extras import sendAWSQuery
from ...services import event_services, place_services, tag_services, event_tag_services


class EventViewsTestCase(TestCase):
    def setUp(self):
        self.form_data = {
            "name": "Test Event",
            "description": "Test Description",
            "image": "Test Image",
            "tags": "test_tag1, test_tag2, test_tag3"
        }
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.events_url = reverse("events")
        self.delete_event_url = reverse("delete_event", args=["1"])
        self.edit_event_url = reverse("edit_event", args=["1"])
        self.add_place_to_event_url = reverse(
            "add_place_to_event", args=["1", "1"])
        self.remove_place_from_event_url = reverse(
            "remove_place_from_event", args=["1", "1"])

    def tearDown(self):
        super().tearDown()
        events = event_services.get_events_list()
        test_event = next(
            (event for event in events if event["name"] == "Test Event"), None)
        if test_event:
            event_services.delete_event(test_event["id"])

        test_place = next(
            (place for place in place_services.get_places_list() if place["name"] == "test Place"), None)
        if test_place:
            place_services.delete_place(test_place["id"])

        tag_services.delete_tag("test_tag1")
        tag_services.delete_tag("test_tag2")
        tag_services.delete_tag("test_tag3")

        events = event_services.get_events_list()
        test_event = next(
            (event for event in events if event["name"] == "Test Event"), None)
        if test_event:
            event_tag_services.delete_tags(test_event["id"])

    def test_all_events_view_not_logged_in_get(self):
        response = self.client.get(self.events_url, follow=True)
        self.assertRedirects(response, reverse("login") + "?next=/events/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_all_events_view_not_logged_in_post_valid_form(self):
        response = self.client.post(
            self.events_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/events/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_all_events_view_not_logged_in_post_invalid_form(self):
        response = self.client.post(self.events_url, {
            "name": "Test Event",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/events/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_all_events_view_get_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.get(self.events_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_events.html")
        self.assertIn("events", response.context)
        self.assertIn("form", response.context)

    def test_all_events_view_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(
            self.events_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_events.html")
        self.assertIn("events", response.context)
        self.assertIn("form", response.context)

    def test_all_events_view_with_valid_form_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        count = len(event_services.get_events_list())
        response = self.client.post(
            self.events_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_events.html")
        self.assertEqual(len(event_services.get_events_list()), count + 1)
        self.assertIn("Event created successfully", [
                      m.message for m in response.context['messages']])
        self.assertIn("events", response.context)
        self.assertIn("form", response.context)

    def test_all_events_view_with_invalid_form_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(self.events_url, {
            "name": "Test Event",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_events.html")
        self.assertIn("Event not created, check formatting", [
            m.message for m in response.context['messages']])
        self.assertIn("events", response.context)
        self.assertIn("form", response.context)

    def test_delete_event_view_not_logged_in_get(self):
        response = self.client.get(self.delete_event_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/events/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_delete_event_view_not_logged_in_post(self):
        response = self.client.post(self.delete_event_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/events/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_delete_event_view_logged_in_get(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.get(self.delete_event_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("events"))
        self.assertIn("Event deleted successfully", [
                      m.message for m in response.context['messages']])

    def test_delete_event_view_logged_in_post(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(self.delete_event_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("events"))
        self.assertIn("Event deleted successfully", [
                      m.message for m in response.context['messages']])

    def test_edit_event_view_not_logged_in_get(self):
        add_event = f"""
            mutation createEvent {{
                createEvent(input: {{
                    id: "1",
                    name: "Test Event",
                    description: "Test Description",
                    image: "Test Image"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_event)

        response = self.client.get(self.edit_event_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/events/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_edit_event_view_not_logged_in_post_valid_form(self):
        add_event = f"""
            mutation createEvent {{
                createEvent(input: {{
                    id: "1",
                    name: "Test Event",
                    description: "Test Description",
                    image: "Test Image"
                }}) {{
                    id
                }}  
            }}
        """
        sendAWSQuery(add_event)

        response = self.client.post(
            self.edit_event_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/events/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_edit_event_view_not_logged_in_post_invalid_form(self):
        add_event = f"""
            mutation createEvent {{
                createEvent(input: {{
                    id: "1",
                    name: "Test Event",
                    description: "Test Description",
                    image: "Test Image"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_event)

        response = self.client.post(self.edit_event_url, {
            "name": "Test Event",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/events/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_edit_event_view_get_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        add_event = f"""
            mutation createEvent {{
                createEvent(input: {{
                    id: "1",
                    name: "Test Event",
                    description: "Test Description",
                    image: "Test Image"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_event)

        response = self.client.get(self.edit_event_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/edit_event.html")
        self.assertIn("form", response.context)

    def test_edit_event_with_valid_form_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        add_event = f"""
            mutation createEvent {{
                createEvent(input: {{ 
                    id: "1",
                    name: "Test Event",
                    description: "Test Description",
                    image: "Test Image"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_event)

        response = self.client.post(
            self.edit_event_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/show_events.html")
        messages = [m.message for m in response.context['messages']]
        self.assertTrue(
            any('"Test Event" edited successfully' in message for message in messages))

    def test_edit_event_with_invalid_form_post_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        add_event = f"""
            mutation createEvent {{
                createEvent(input: {{ 
                    id: "1",
                    name: "Test Event",
                    description: "Test Description",
                    image: "Test Image"
                }}) {{
                    id
                }}
            }}
        """
        sendAWSQuery(add_event)

        response = self.client.post(self.edit_event_url, {
            "name": "Test Event"
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/edit_event.html")
        self.assertIn("form", response.context)

    def test_add_place_to_event_view_not_logged_in_get(self):
        response = self.client.get(self.add_place_to_event_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/events/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_add_place_to_event_view_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(self.add_place_to_event_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("events"))
        self.assertIn("Place assigned successfully", [
                      m.message for m in response.context['messages']])

    def test_remove_place_from_event_view_not_logged_in_get(self):
        response = self.client.get(
            self.remove_place_from_event_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=/events/")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_remove_place_from_event_view_logged_in(self):
        login = self.client.login(
            username=self.user.username, password='testpass123')
        self.assertTrue(login)

        response = self.client.post(
            self.remove_place_from_event_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("events"))
        self.assertIn("Place detached successfully", [
                      m.message for m in response.context['messages']])
