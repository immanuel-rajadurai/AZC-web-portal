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
                    scientificName
                    habitat
                    diet
                    behaviour
                    weightMale
                    weightFemale
                    image
                    conservationStatus
                    funFacts
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
    if response.json()["data"]:
        return response.json()["data"]["listAnimals"]["items"]

    return []


def add_animal(name, scientificName, habitat, diet, behaviour, weightMale, weightFemale, image, conservationStatus, funFacts):
    payload = {
        'query': f"""
            mutation createAnimal {{
                createAnimal(input: {{ 
                    name: "{name}", 
                    scientificName: "{scientificName}", 
                    habitat: "{habitat}", 
                    diet: "{diet}", 
                    behaviour: "{behaviour}", 
                    weightMale: "{weightMale}", 
                    weightFemale: "{weightFemale}", 
                    image: "{image}", 
                    conservationStatus: "{conservationStatus}", 
                    funFacts: "{funFacts}" 
                }} ) {{
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
                query listPlaceAnimals {{
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


def edit_animal(animal_id, name, scientificName, habitat, diet, behaviour, weightMale, weightFemale, image, conservationStatus, funFacts):
    edit_animal_payload = {
        'query': f"""
            mutation updateAnimal {{
                updateAnimal(input: {{ 
                    id: "{animal_id}", 
                    name: "{name}", 
                    scientificName: "{scientificName}", 
                    habitat: "{habitat}", 
                    diet: "{diet}", 
                    behaviour: "{behaviour}", 
                    weightMale: "{weightMale}", 
                    weightFemale: "{weightFemale}", 
                    image: "{image}", 
                    conservationStatus: "{conservationStatus}", 
                    funFacts: "{funFacts}" 
                }}, condition: null) {{
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
            query getAnimal {{
                getAnimal(id: "{id}") {{
                    name
                    image
                    scientificName
                    habitat
                    diet
                    behaviour
                    weightMale
                    weightFemale
                    image
                    conservationStatus
                    funFacts
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
