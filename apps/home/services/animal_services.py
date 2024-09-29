import requests
import json
from .api_info import *

# The headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}


def get_animals_list():
    list_animals = """
        query listAnimals {
            listAnimals {
                items {
                    id
                    name
                    image
                }
            }
        }
    """

    # The payload for the HTTP request
    payload = {
        'query': list_animals
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    # print(response.json())
    if response.json()["data"] != None:
        return response.json()["data"]["listAnimals"]["items"]

    return None


def add_animal(name, image):
    payload = {
        'query': f"""
            mutation createAnimal {{
                createAnimal(input: {{name: "{name}", image: "{image}"}}) {{
                    id
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))
    # print(response.json())


def remove_animal(id):
    remove_animal_payload = {
        'query': f"""
            mutation deleteAnimal {{
                deleteAnimal(input: {{id: "{id}"}}) {{
                    id
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(remove_animal_payload))
    # print(response.json())


def edit_animal(animal_id, name, image):
    edit_animal_payload = {
        'query': f"""
            mutation updateAnimal {{
                updateAnimal(input: {{id: "{animal_id}", name: "{name}", image: "{image}"}}, condition: null) {{
                    id
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(edit_animal_payload))
    # print(response.json())


def get_animal(id):
    payload = {
        'query': f"""
            query listAnimals {{
                getAnimal(id: "{id}") {{
                    name
                    image
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    # print(response.json())
    if response.json()["data"] != None:
        return response.json()["data"]["getAnimal"]

    return None
