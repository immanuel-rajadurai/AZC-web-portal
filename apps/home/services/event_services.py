from .services_extras import *
import json

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

    return sendAWSQuery(list_events).json()["data"]["listEvents"]["items"]


def create_event(name, description, image):
    create_event_query = f"""
        mutation CreateEvent {{
            createEvent(input: {{
                name: {json.dumps(name)},
                image: {json.dumps(image)},
                description: {json.dumps(description)}
            }}) {{
                id
            }}
        }}
    """
    response = sendAWSQuery(create_event_query).json()

    if 'errors' in response:
        print(f"GraphQL errors: {response['errors']}")
        raise Exception("Failed to create event")

    return response['data']['createEvent']['id']


def delete_attached_relationships(event_id):
    get_relationships = f"""
        query listEventPlaces {{
            listEventPlaces(filter: {{ eventID: {{eq: "{ event_id }"}} }}) {{
                items {{
                    id
                }}
            }}
        }}
    """

    relationships = sendAWSQuery(get_relationships).json()[
        "data"]["listEventPlaces"]["items"]

    for rel in relationships:
        delete_relationships = f"""
            mutation deleteEventPlace {{
                deleteEventPlace(input: {{id: "{rel['id']}"}}) {{
                    id
                }}
            }}
        """

        sendAWSQuery(delete_relationships)


def delete_event(event_id):
    delete_event = f"""
        mutation deleteEvent {{
            deleteEvent(input: {{id: "{event_id}"}}) {{
                id
            }}
        }}
    """

    sendAWSQuery(delete_event)
    delete_attached_relationships(event_id)


def edit_event(event_id, name, description, image):
    edit_event = f"""
        mutation updateEvent {{
            updateEvent(input: {{
                id: {json.dumps(event_id)},
                name: {json.dumps(name)},
                description: {json.dumps(description)},
                image: {json.dumps(image)}
            }}, condition: null) {{
                id
            }}
        }}
    """

    sendAWSQuery(edit_event)


def get_event(event_id):
    get_event = f"""
        query getEvent {{
            getEvent(id: "{event_id}") {{
                name
                description
                image
            }}
        }}
    """

    return sendAWSQuery(get_event).json()["data"]["getEvent"]
