import requests
import json

API_KEY = 'da2-ewwgqtv4a5fkzc4mh7u4sfxkqu'
APPSYNC_ENDPOINT = """https://g4gxobh45jeqrke2ywuday5sgq.appsync-api.eu-west-2.amazonaws.com/graphql"""

# The headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}

list_places = """
  query ListPlaces {
    listPlaces {
      items {
        id
        name
        description
        animal_id
        isOpen
        image
      }
    }
  }
"""


def get_places_list():

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
    create_place_item = f"""
      mutation CreatePlace {{
        CreatePlace(input: {{name: "{name}", description: "{description}", animal_id: "{animal_id}", isOpen: "{isOpen}", image: "{image}", }}) {{
          id
        }}
      }}
    """

    payload = {
        'query': create_place_item
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    return response.json()


# TODO: add implmentation
# delete_place = """
#   mutation DeletePlace {
#     deletePlace(input: {id: "130749d8-3b8c-4fc3-9d0c-1b63c8e4d5aa"}) {
#       id
#     }
#   }
# """
# def delete_place():
