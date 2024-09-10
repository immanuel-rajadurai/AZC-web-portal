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


def create_place(name, description, isOpen, image):
    payload = {
        'query': f"""
            mutation createPlace {{
                createPlace(input: {{name: "{name}", description: "{description}", isOpen: "{isOpen}", image: "{image}"}}) {{
                    id
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))


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
