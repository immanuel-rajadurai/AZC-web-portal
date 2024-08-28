import requests
import json

API_KEY = 'da2-ewwgqtv4a5fkzc4mh7u4sfxkqu'
APPSYNC_ENDPOINT = """https://g4gxobh45jeqrke2ywuday5sgq.appsync-api.eu-west-2.amazonaws.com/graphql"""

# The headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}

list_animals = """
  query ListAnimals {
    listAnimals {
      items {
        id
        name
        place_id
        animal_id
        image
      }
    }
  }
"""


def get_animals_list():

    # The payload for the HTTP request
    payload = {
        'query': list_animals
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    print(response.json())

    return response.json()["data"]["listAnimals"]["items"]


def add_animal(name, place_id, image=None):
    add_animal_item = f"""
      mutation AddAnimal {{
        addAnimal(input: {{name: "{name}", place_id: "{place_id}", image: "{image}"}}) {{
          id
        }}
      }}
    """

    payload = {
        'query': add_animal_item
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    return response.json()


# FIXME: implement deletion PROPERLY with graphql
def delete_animal(id):
    delete_animal_mutation = f"""
      mutation DeleteAnimal {{
        deleteAnimal(input: {{id: "{id}"}}) {{
        }}
      }}
    """

    payload = {
        'query': delete_animal_mutation
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    return response.json()
