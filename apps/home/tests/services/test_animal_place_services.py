from django.test import TestCase
import json

from ...services import animal_place_services, animal_services, place_services

from ...services.services_extras import *


class AnimalPlaceServicesTestCase(TestCase):
    def delete_test_place_and_animal(self):
        places = place_services.get_places_list()
        place = next((place for place in places if place['name'] == 'TEST'), None)
        place_services.delete_place(place['id']) if place else None

        animals = animal_services.get_animals_list()
        animal = next((animal for animal in animals if animal['name'] == 'TEST'), None)
        animal_services.remove_animal(animal['id']) if animal else None

    def setUp(self):
        place_services.create_place('TEST', 'testing place', True, 'https://www.google.com')
        animal_services.add_animal('TEST', 'testing scientificName', 'testing habitat', 'testing diet', 'testing behaviour', 'testing weightMale', 'testing weightFemale', 'https://www.google.com', 'testing conservationStatus', 'testing funFacts')

    def tearDown(self):
        super().tearDown()
        self.delete_test_place_and_animal()

    def get_test_animal(self):
        animals = animal_services.get_animals_list()
        return next((animal for animal in animals if animal['name'] == 'TEST'), None)
    
    def get_test_place(self):
        places = place_services.get_places_list()
        return next((place for place in places if place['name'] == 'TEST'), None)
    
    def test_get_testing_animals(self):
        animal = self.get_test_animal()

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

    def test_get_testing_place(self):
        place = self.get_test_place()

        place = place_services.get_place(place['id'])
        self.assertEqual(place['name'], 'TEST')
        self.assertEqual(place['description'], 'testing place')
        self.assertEqual(place['isOpen'], True)
        self.assertEqual(place['image'], 'https://www.google.com')

    def test_get_animals_linked_to_place(self):
        place = self.get_test_place()

        animals = animal_place_services.get_animals_linked_to_place(place['id'])
        self.assertEqual(animals, [])

    def test_add_animal_to_place(self):
        place = self.get_test_place()
        animal = self.get_test_animal()

        animal_place_services.add_animal_to_place(animal['id'], place['id'])
        animals = animal_place_services.get_animals_linked_to_place(place['id'])
        self.assertEqual(animals, [{'animalID': animal['id']}])

    def test_remove_animal_from_place(self):
        place = self.get_test_place()
        animal = self.get_test_animal()

        animal_place_services.remove_animal_from_place(animal['id'], place['id'])
        animals = animal_place_services.get_animals_linked_to_place(place['id'])
        self.assertEqual(animals, [])