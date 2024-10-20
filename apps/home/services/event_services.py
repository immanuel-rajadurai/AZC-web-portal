import requests
import json
from .api_info import *

headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}


def get_events_list():
    list_events = """
        query listEvents {
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

    payload = {
        'query': list_events
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    # print(response.json())
    if response.json()["data"]:
        return response.json()["data"]["listEvents"]["items"]

    return []


def create_event(name, description, image):
    create_event_mutation = f"""
        mutation createEvent {{
            createEvent(input: {{name: "{name}", image: "{image}", description: "{description}"}}) {{
                id
            }}
        }}
    """

    payload = {
        'query': create_event_mutation
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))
    return response.json()['data']['createEvent']['id']


def delete_attached_relationships(event_id):
    get_rel_payload = {
        'query': f"""
                query listEventPlaces {{
                    listEventPlaces(filter: {{ eventID: {{eq: "{ event_id }"}} }}) {{
                        items {{
                            id
                        }}
                    }}
                }}
            """
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(get_rel_payload))

    rels = response.json()["data"]["listEventPlaces"]["items"]

    for rel in rels:
        delete_rel_payload = {
            'query': f"""
                mutation deleteEventPlace {{
                    deleteEventPlace(input: {{id: "{rel['id']}"}}) {{
                        id
                    }}
                }}
            """
        }

        response2 = requests.post(
            APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_rel_payload))
        # print("response2.json(): ", response2.json())


def delete_event(event_id):
    delete_event_payload = {
        'query': f"""
            mutation deleteEvent {{
                deleteEvent(input: {{id: "{event_id}"}}) {{
                    id
                }}
            }}
        """
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_event_payload))
    # print(response.json())

    delete_attached_relationships(event_id)


def edit_event(event_id, name, description, image):
    edit_event_payload = {
        'query': f"""
            mutation updateEvent {{
                updateEvent(input: {{id: "{event_id}", name: "{name}", description: "{description}", image: "{image}"}}, condition: null) {{
                    id
                }}
            }}
        """
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(edit_event_payload))
    # print(response.json())


def get_event(event_id):
    payload = {
        'query': f"""
            query getEvent {{
                getEvent(id: "{event_id}") {{
                    name
                    description
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
        return response.json()["data"]["getEvent"]

    return []
