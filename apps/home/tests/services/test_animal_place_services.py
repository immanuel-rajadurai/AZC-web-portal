from unittest import TestCase

from ...services import AnimalPlaceServices

class AnimalPlaceServices(TestCase):
    def setUp(self):
        self.service = AnimalPlaceServices()
        
    def test_add_animal_to_place(self):
        #compare animals added to place before and after
        self.service.add_animal_to_place('animal_id', 'place_id')
    

        
    def test_remove_animal_from_place(self):
        #compare animals added to place before and after
        self.service.remove_animal_from_place('animal_id', 'place_id')
