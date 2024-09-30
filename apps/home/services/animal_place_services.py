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


def get_animals_linked_to_place(place_id):
    payload = {
        'query': f"""
            query listPlaceAnimal {{
                getPlaceAnimal(placeID: "{place_id}") {{
                    animalID
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    # print(response.json())
    if response.json()["data"] != None:
        return response.json()["data"]["listPlaceAnimal"]

    return None


def remove_animal_from_place(animal_id, place_id):
    delete_rel_payload = {
        'query': f"""
            mutation deletePlaceAnimal {{
                deletePlaceAnimal(input: {{animalID: "{animal_id}", placeID:"{place_id}"}}) {{
                    id
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_rel_payload))
    # print(response.json())
