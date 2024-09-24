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
        query listPlaces {
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

    # print(response.json())
    return response.json()["data"]["listPlaces"]["items"]


def create_place(name, description, isOpen, image):

    print("calling create place")

    # payload = f'''
    #             mutation {{
    #                 createPlace(input: {{
    #                     description: "{description}",
    #                     image: "{image}",
    #                     isOpen: {str(isOpen).lower()},
    #                     name: "{name}"
    #                 }}) {{
    #                     id
    #                     description
    #                     image
    #                     isOpen
    #                     name
    #                 }}
    #             }}
    #             '''

    payload = {
        'query': f"""
            mutation createPlace {{
                createPlace(input: {{name: "{name}", description: "{description}", isOpen: {str(isOpen).lower()}, image: "{image}"}}) {{
                    id
                }}
            }}
        """
    }

    response = requests.post(APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    print("create place response: ", response.json())


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
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_place_payload))
    # print(response.json())


def edit_place(place_id, name, description, isOpen, image):
    edit_place_payload = {
        'query': f"""
            mutation updatePlace {{
                updatePlace(input: {{id: "{place_id}", name: "{name}", description: "{description}", isOpen: "{isOpen}", image: "{image}"}}, condition: null) {{
                    id
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(edit_place_payload))
    # print(response.json())


def get_place(id):
    payload = {
        'query': f"""
            query listPlaces {{
                getPlace(id: "{id}") {{
                    name
                    description
                    isOpen
                    image
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    # print(response.json())
    return response.json()["data"]["getPlace"]
