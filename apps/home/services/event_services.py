import requests
import json
from .api_info import *

# The headers for the HTTP request
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

    # The payload for the HTTP request
    payload = {
        'query': list_events
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    # print(response.json())
    if response.json()["data"] != None:
        return response.json()["data"]["listEvents"]["items"]

    return None


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

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))
    return response.json()


# def create_event_and_place(name, description, place_id, image=None):
#     if image != None:
#         create_event_payload = {
#             'query': f"""
#                 mutation createEvent {{
#                     createEvent(input: {{id: {id},
#                         name: "{name},
#                         description: {description},
#                         image: {image}}}) {{
#                         id
#                     }}
#                 }}
#             """
#         }
#     else:
#         create_event_payload = {
#             'query': f"""
#                 mutation createEvent {{
#                     createEvent(input: {{id: {id},
#                         name: "{name},
#                         description: {description}}}) {{
#                             id
#                     }}
#                 }}
#             """
#         }
#     response = requests.post(
#         APPSYNC_ENDPOINT, headers=headers, data=json.dumps(create_event_payload))

#     event_id = response.json()["data"]["createEvent"]["id"]
#     create_event_place_payload = {
#         'query': f"""
#             mutation createEventPlace {{
#                 createEventPlace(input: {{
#                     placeID: "{place_id},
#                     eventID: {event_id}}}) {{
#                         id
#                 }}
#             }}
#         """
#     }
#   response = requests.post(
#         APPSYNC_ENDPOINT, headers=headers, data=json.dumps(create_event_place_payload))
    # print(response.json())


def delete_event(id):
    delete_event_payload = {
        'query': f"""
            mutation deleteEvent {{
                deleteEvent(input: {{id: "{id}"}}) {{
                    id
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_event_payload))
    # print(response.json())


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

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(edit_event_payload))
    # print(response.json())


def get_event(id):
    payload = {
        'query': f"""
            query listEvents {{
                getEvent(id: "{id}") {{
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
    if response.json()["data"] != None:
        return response.json()["data"]["getEvent"]

    return None
