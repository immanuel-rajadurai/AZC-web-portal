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
    if response.json()["data"]:
        return response.json()["data"]["listAnimals"]["items"]

    return []


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


def delete_attached_relationships(animal_id):
    get_rel_payload = {
        'query': f"""
                query listPlaceAnimal {{
                    listPlaceAnimals(filter: {{ animalID: {{eq: "{ animal_id }"}} }}) {{
                        items {{
                            id
                        }}
                    }}
                }}
            """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(get_rel_payload))

    rel_id = response.json()["data"]["listPlaceAnimals"]["items"][0]['id']
    # print("rel_id: ", rel_id)

    delete_rel_payload = {
        'query': f"""
            mutation deletePlaceAnimal {{
                deletePlaceAnimal(input: {{id: "{rel_id}"}}) {{
                    id
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response2 = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_rel_payload))
    # print("response2.json(): ", response2.json())


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

    delete_attached_relationships(id)


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
    if response.json()["data"]:
        return response.json()["data"]["getAnimal"]

    return []
