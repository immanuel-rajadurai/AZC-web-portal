import requests
import json
from .api_info import *

# The headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}


def add_animal_to_place(animal_id, place_id):
    create_animal_place_payload = {
        'query': f"""
            mutation createPlaceAnimal {{
                createPlaceAnimal(input: {{
                    placeID: "{place_id}",
                    animalID: "{animal_id}"}}) {{
                        id
                }}
            }}
        """
    }
    requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(create_animal_place_payload))
