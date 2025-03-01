from django.test import TestCase
from ...services import place_services


class PlaceServicesTestCase(TestCase):
    def delete_test_place(self):
        places = place_services.get_places_list()
        place = next((place for place in places if place["name"] == "TEST"), None)
        place_services.delete_place(place["id"]) if place else None

        places = place_services.get_places_list()
        place = next((place for place in places if place["name"] == "TEST2"), None)
        place_services.delete_place(place["id"]) if place else None

    def setUp(self):
        place_services.create_place(
            "TEST", "testing description", True, "https://www.google.com"
        )

    def tearDown(self):
        super().tearDown()
        self.delete_test_place()

    def get_test_place(self):
        places = place_services.get_places_list()
        return next((place for place in places if place["name"] == "TEST"), None)

    def test_get_places_list(self):
        places = place_services.get_places_list()
        self.assertNotEqual(places, [])

    def test_create_place(self):
        place = self.get_test_place()

        self.assertIsNotNone(place)
        self.assertEqual(place["name"], "TEST")
        self.assertEqual(place["description"], "testing description")
        self.assertEqual(place["isOpen"], True)
        self.assertEqual(place["image"], "https://www.google.com")

    def test_delete_place(self):
        place = self.get_test_place()
        id = place["id"]
        self.assertIsNotNone(place)

        place_services.delete_place(place["id"])

        place2 = self.get_test_place()
        self.assertIsNone(place2)

        attached_relationships = place_services.get_attached_relationships(id)
        self.assertEqual(attached_relationships, [])

    def test_edit_place(self):
        place = self.get_test_place()
        self.assertIsNotNone(place)
        self.assertEqual(place["name"], "TEST")
        self.assertEqual(place["description"], "testing description")
        self.assertEqual(place["isOpen"], True)
        self.assertEqual(place["image"], "https://www.google.com")

        place_services.edit_place(
            place["id"],
            "TEST2",
            "testing description2",
            False,
            "https://www.google2.com",
        )
        place2 = place_services.get_place(place["id"])

        self.assertEqual(place2["name"], "TEST2")
        self.assertEqual(place2["description"], "testing description2")
        self.assertEqual(place2["isOpen"], False)
        self.assertEqual(place2["image"], "https://www.google2.com")

    def test_get_place(self):
        place = self.get_test_place()
        self.assertIsNotNone(place)
        self.assertEqual(place["name"], "TEST")
        self.assertEqual(place["description"], "testing description")
        self.assertEqual(place["isOpen"], True)
        self.assertEqual(place["image"], "https://www.google.com")
