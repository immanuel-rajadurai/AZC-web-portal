import requests
import json
from api_info import *

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
        description
        name
        image
      }
    }
  }
"""


def get_events_list():
    list_events = """
        query ListEvents {
            listEvents {
                items {
                    id
                    name
                    description
                    image
                }
            }
        }
    """

    # The payload for the HTTP request
    payload = {
        'query': list_events
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    print(response.json())

    return response.json()["data"]["listEvents"]["items"]


def create_event(name, description, place_id=None, image=None):
    if image != None:
        create_event_payload = {
            'query': f"""
                mutation createEvent {{
                    createEvent(input: {{id: {id},
                        name: "{name},
                        description: {description},
                        image: {image}}}) {{
                        id
                    }}
                }}
            """
        }
    else:
        create_event_payload = {
            'query': f"""
                mutation createEvent {{
                    createEvent(input: {{id: {id},
                        name: "{name},
                        description: {description}}}) {{
                            id
                    }}
                }}
            """
        }
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(create_event_payload))

    if place_id != None:
        event_id = response.json()["data"]["createEvent"]["id"]
        create_place_animal_payload = {
            'query': f"""
                mutation createEventPlace {{
                    createEventPlace(input: {{
                        placeID: "{place_id},
                        eventID: {event_id}}}) {{
                            id
                    }}
                }}
            """
        }
        requests.post(
            APPSYNC_ENDPOINT, headers=headers, data=json.dumps(create_place_animal_payload))


def delete_event(id):
    delete_event_payload = {
        'query': f"""
            mutation deleteEvent {{
               deleteEvent(input: {{id: {id}}}) {{
                 id
               }}
            }}
      """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_event_payload))
