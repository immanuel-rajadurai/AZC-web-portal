import requests
import json
from .api_info import *

# The headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}


def get_places_list():
    list_places = """
        query ListPlaces {
            listPlaces {
                items {
                    id
                    name
                    description
                    isOpen
                    image
                }
            }
        }
    """

    # The payload for the HTTP request
    payload = {
        'query': list_places
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    print(response.json())

    return response.json()["data"]["listPlaces"]["items"]


def create_place(name, description, isOpen, animal_id=None, image=None):
    if image != None:
        create_place_payload = {
            'query': f"""
                mutation createPlace {{
                    createPlace(input: {{
                    name: "{name}, description: {description}, 
                        image: {image}, 
                        isOpen: {isOpen}}}) {{
                            id
                    }}
                }}
            """
        }
    else:
        create_place_payload = {
            'query': f"""
                mutation createPlace {{
                    createPlace(input: {{
                    name: "{name}, description: {description}, 
                        isOpen: {isOpen}}}) {{
                            id
                    }}
                }}
            """
        }
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(create_place_payload))

    if animal_id != None:
        place_id = response.json()["data"]["createPlace"]["id"]
        create_place_animal_payload = {
            'query': f"""
                mutation createPlaceAnimal {{
                    createPlaceAnimal(input: {{
                        animalID: "{animal_id},
                        placeID: {place_id}}}) {{
                            id
                    }}
                }}
            """
        }
        requests.post(
            APPSYNC_ENDPOINT, headers=headers, data=json.dumps(create_place_animal_payload))


def delete_place(id):
    delete_place_payload = {
        'query': f"""
            mutation deletePlace {{
                deletePlace(input: {{id: "{id}"}}) {{
                    id
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_place_payload))
