import requests
import json
from .api_info import *

# The headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}


def add_event_to_place(event_id, place_id):
    create_event_place_payload = {
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
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(create_event_place_payload))
