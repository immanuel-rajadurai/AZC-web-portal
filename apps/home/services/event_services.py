import requests
import json
from api_info import *

APPSYNC_ENDPOINT = """https://g4gxobh45jeqrke2ywuday5sgq.appsync-api.eu-west-2.amazonaws.com/graphql"""

# The headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}

list_events = """
  query ListEvents {
    listEvents {
      items {
        id
        name
        description
        place_id
        animal_id
        image
      }
    }
  }
"""


def get_events_list():

    # The payload for the HTTP request
    payload = {
        'query': list_events
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    print(response.json())

    return response.json()["data"]["listEvents"]["items"]


def create_event(name, description, place_id, image=None, animal_id=None):
    create_event_item = f"""
      mutation CreateEvent {{
        createEvent(input: {{name: "{name}", description: "{description}", place_id: "{place_id}", animal_id: "{animal_id}", image: "{image}"}}) {{
          id
        }}
      }}
    """

    payload = {
        'query': create_event_item
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    return response.json()


# TODO: add implmentation
# delete_event = """
#   mutation DeleteEvent {
#     deleteEvent(input: {id: "130749d8-3b8c-4fc3-9d0c-1b63c8e4d5aa"}) {
#       id
#     }
#   }
# """
# def delete_event():
