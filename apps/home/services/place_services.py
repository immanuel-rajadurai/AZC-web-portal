import requests
import json
from api_info import *

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
                    animal_id
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
    create_place_payload = {
        'query': f"""
            mutation createPlace {{
               createPlace(input: {{id: {id}, 
                name: "{name}, 
                description: {description}, 
                image: {image}, 
                isOpen: {isOpen}, 
                placeAnimalId: {animal_id}}}) {{
                 id
               }}
            }}
      """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(create_place_payload))

    return response.json()


def delete_place(id):
    delete_place_mutation = f"""
      mutation deletePlace {{
        deletePlace(input: {{id: "{id}"}}) {{
        }}
      }}
    """

    payload = {
        'query': delete_place_mutation
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    return response.json()
