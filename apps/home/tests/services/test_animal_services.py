from django.test import TestCase
import json

from ...services import animal_services

from ...services.services_extras import *

class AnimalServicesTestCase(TestCase):
    def delete_test_animal(self):
        animals = animal_services.get_animals_list()
        animal = next((animal for animal in animals if animal['name'] == 'TEST'), None)
        animal_services.remove_animal(animal['id']) if animal else None

    def setUp(self):
        animal_services.add_animal('TEST', 'testing scientificName', 'testing habitat', 'testing diet', 'testing behaviour', 'testing weightMale', 'testing weightFemale', 'https://www.google.com', 'testing conservationStatus', 'testing funFacts')

    def tearDown(self):
        super().tearDown()
        self.delete_test_animal()

    def get_test_animal(self):
        animals = animal_services.get_animals_list()
        return next((animal for animal in animals if animal['name'] == 'TEST'), None)

    def test_get_animals_list(self):
        animals = animal_services.get_animals_list()
        self.assertNotEqual(animals, [])

    def test_add_animal(self):        
        animal = self.get_test_animal()
        self.assertIsNotNone(animal)

        self.assertIsNotNone(animal)
        self.assertEqual(animal['name'], 'TEST')
        self.assertEqual(animal['scientificName'], 'testing scientificName')
        self.assertEqual(animal['habitat'], 'testing habitat')
        self.assertEqual(animal['diet'], 'testing diet')
        self.assertEqual(animal['behaviour'], 'testing behaviour')
        self.assertEqual(animal['weightMale'], 'testing weightMale')
        self.assertEqual(animal['weightFemale'], 'testing weightFemale')
        self.assertEqual(animal['image'], 'https://www.google.com')
        self.assertEqual(animal['conservationStatus'], 'testing conservationStatus')
        self.assertEqual(animal['funFacts'], 'testing funFacts')

    def test_remove_animal(self):        
        animal = self.get_test_animal()
        id = animal['id']
        self.assertIsNotNone(animal)

        animal_services.remove_animal(animal['id'])

        animal2 = animal_services.get_animal(id)
        self.assertIsNone(animal2)

        attached_relationships = animal_services.get_attached_relationships(id)
        self.assertEqual(attached_relationships, [])

    def test_get_animal(self):
        animal = self.get_test_animal()
        self.assertIsNotNone(animal)

        animal2 = animal_services.get_animal(animal['id'])
        self.assertEqual(animal2['name'], 'TEST')
        self.assertEqual(animal2['scientificName'], 'testing scientificName')
        self.assertEqual(animal2['habitat'], 'testing habitat')
        self.assertEqual(animal2['diet'], 'testing diet')
        self.assertEqual(animal2['behaviour'], 'testing behaviour')
        self.assertEqual(animal2['weightMale'], 'testing weightMale')
        self.assertEqual(animal2['weightFemale'], 'testing weightFemale')
        self.assertEqual(animal2['image'], 'https://www.google.com')
        self.assertEqual(animal2['conservationStatus'], 'testing conservationStatus')
        self.assertEqual(animal2['funFacts'], 'testing funFacts')
