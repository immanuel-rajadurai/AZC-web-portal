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
                listEventPlaces(filter: {{ eventID: {{eq: "{ event_id }"}} }}) {{
                    items {{
                        placeID
                    }}
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    tmp = response.json()["data"]["listEventPlaces"]["items"]
    print("tmp: ", tmp)

    if tmp:
        print("listEventPlace: ", tmp)
        return tmp

    return None


def remove_place_from_event(place_id, event_id):
    get_rel_payload = {
        'query': f"""
            query ListEventPlacesFilter {{
                listEventPlaces(filter: {{eventID: {{eq: "{event_id}"}}, placeID: {{eq: "{place_id}"}}}}) {{
                    items {{
                        id
                    }}
                }}
            }}
        """
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(get_rel_payload))
    # print("response.json():", response.json())

    rel_id = response.json()["data"]["listEventPlaces"]["items"][0]['id']
    # print("rel_id: ", rel_id)

    delete_rel_payload = {
        'query': f"""
            mutation deleteEventPlace {{
                deleteEventPlace(input: {{id: "{rel_id}"}}) {{
                    id
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response2 = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_rel_payload))
    # print("response2.json(): ", response2.json())
