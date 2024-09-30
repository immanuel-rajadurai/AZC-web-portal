import requests
import json
from .api_info import *

# The headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}


def add_place_to_event(event_id, place_id):
    create_event_place_payload = {
        'query': f"""
            mutation createEventPlace {{
                createEventPlace(input: {{
                    placeID: "{place_id}",
                    eventID: "{event_id}"}}) {{
                        id
                }}
            }}
        """
    }
    requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(create_event_place_payload))


def get_places_linked_to_event(event_id):
    payload = {
        'query': f"""
            query listEventPlace {{
                getEventPlace(eventID: "{event_id}") {{
                    placeID
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    # print(response.json())
    if response.json()["data"] != None:
        return response.json()["data"]["getEventPlace"]

    return None


def remove_place_from_event(place_id, event_id):
    delete_rel_payload = {
        'query': f"""
            mutation deleteEventPlace {{
                deleteEventPlace(input: {{placeID: "{place_id}", eventID:"{event_id}"}}) {{
                    id
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_rel_payload))
    # print(response.json())
