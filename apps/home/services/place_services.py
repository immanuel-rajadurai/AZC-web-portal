import requests
import json
from .api_info import *

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

    payload = {
        'query': list_places
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    # print(response.json())
    if response.json()["data"]:
        return response.json()["data"]["listPlaces"]["items"]

    return []


def create_place(name, description, isOpen, image):
    payload = {
        'query': f"""
            mutation createPlace {{
                createPlace(input: {{name: "{name}", description: "{description}", isOpen: {str(isOpen).lower()}, image: "{image}"}}) {{
                    id
                }}
            }}
        """
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    # print("create place response: ", response.json())


def delete_attached_relationships(place_id):
    get_rel_payload = {
        'query': f"""
                query listPlaceAnimals {{
                    listPlaceAnimals(filter: {{ placeID: {{eq: "{ place_id }"}} }}) {{
                        items {{
                            id
                        }}
                    }}
                }}
            """
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(get_rel_payload))

    rels = response.json()["data"]["listPlaceAnimals"]["items"]

    for rel in rels:
        delete_rel_payload = {
            'query': f"""
                mutation deletePlaceAnimal {{
                    deletePlaceAnimal(input: {{id: "{rel['id']}"}}) {{
                        id
                    }}
                }}
            """
        }

        response2 = requests.post(
            APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_rel_payload))
        # print("response2.json(): ", response2.json())

    get_rel_payload2 = {
        'query': f"""
                query listEventPlaces {{
                    listEventPlaces(filter: {{ placeID: {{eq: "{ place_id }"}} }}) {{
                        items {{
                            id
                        }}
                    }}
                }}
            """
    }

    response3 = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(get_rel_payload2))

    rel_id = response3.json()["data"]["listEventPlaces"]["items"]['id']
    # print("rel_id: ", rel_id)

    delete_rel_payload2 = {
        'query': f"""
            mutation deleteEventPlace {{
                deleteEventPlace(input: {{id: "{rel_id}"}}) {{
                    id
                }}
            }}
        """
    }

    response4 = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_rel_payload2))
    # print("response4.json(): ", response4.json())


def delete_place(place_id):
    delete_place_payload = {
        'query': f"""
            mutation deletePlace {{
                deletePlace(input: {{id: "{place_id}"}}) {{
                    id
                }}
            }}
        """
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_place_payload))
    # print(response.json())

    delete_attached_relationships(place_id)


def edit_place(place_id, name, description, isOpen, image):
    edit_place_payload = {
        'query': f"""
            mutation updatePlace {{
                updatePlace(input: {{id: "{place_id}", name: "{name}", description: "{description}", isOpen: {str(isOpen).lower()}, image: "{image}"}}, condition: null) {{
                    id
                }}
            }}
        """
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(edit_place_payload))
    # print(response.json())


def get_place(place_id):
    payload = {
        'query': f"""
            query getPlace {{
                getPlace(id: "{place_id}") {{
                    name
                    description
                    isOpen
                    image
                }}
            }}
        """
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    # print(response.json())
    return response.json()["data"]["getPlace"]
