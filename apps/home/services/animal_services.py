import requests
import json
from api_info import *

# The headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}


def get_animals_list():
    list_animals = """
        query ListAnimals {
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

    print(response.json())

    return response.json()["data"]["listAnimals"]["items"]


def add_animal(name, image=None):
    create_animal_payload = {
        'query': f"""
                mutation createAnimal {{
                  createAnimal(input: {{id: {id}, image: {image}, name: {name}}}) {{
                    id
                  }}
                }}
        """
    }

    # Send the POST request to the AppSync endpoint
    requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(create_animal_payload))


def delete_animal(id):
    delete_animal_mutation = f"""
      mutation deleteAnimal {{
        deleteAnimal(input: {{id: "{id}"}}) {{
        }}
      }}
    """

    payload = {
        'query': delete_animal_mutation
    }

    # Send the POST request to the AppSync endpoint
    requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))
