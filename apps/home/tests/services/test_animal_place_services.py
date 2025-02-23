from unittest import TestCase

from ...services import AnimalPlaceServices

class AnimalPlaceServices(TestCase):
    def setUp(self):
        self.service = AnimalPlaceServices()
        
    def test_add_animal_to_place(self):
        self.service.add_animal_to_place('animal_id', 'place_id')
        
    def test_get_animals_linked_to_place(self):
        self.service.get_animals_linked_to_place('place_id')
        
    def test_remove_animal_from_place(self):
        self.service.remove_animal_from_place('animal_id', 'place_id')