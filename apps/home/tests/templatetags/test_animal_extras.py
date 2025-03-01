from django.test import TestCase

from ...templatetags import animal_extras
from ...services import animal_services


class AnimalExtrasTestCase(TestCase):
    def delete_test_animal(self):
        animals = animal_services.get_animals_list()
        animal = next((animal for animal in animals if animal["name"] == "TEST"), None)
        animal_services.remove_animal(animal["id"]) if animal else None

    def get_test_animal(self):
        animals = animal_services.get_animals_list()
        return next((animal for animal in animals if animal["name"] == "TEST"), None)

    def setUp(self):
        animal_services.add_animal(
            "TEST",
            "testing scientificName",
            "testing habitat",
            "testing diet",
            "testing behaviour",
            "testing weightMale",
            "testing weightFemale",
            "https://www.google.com",
            "testing conservationStatus",
            "testing funFacts",
        )

    def tearDown(self):
        super().tearDown()
        self.delete_test_animal()

    def test_get_animal_name(self):
        animal = self.get_test_animal()
        self.assertIsNotNone(animal)

        self.assertEqual(animal_extras.get_animal_name(animal["id"]), "TEST")

    def test_get_animal_name_undefined(self):
        self.assertEqual(animal_extras.get_animal_name(1234), "Undefined")
