from .services_extras import *


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
    create_event_mutation = f"""
        mutation createEvent {{
            createEvent(input: {{name: "{name}", image: "{image}", description: "{description}"}}) {{
                id
            }}
        }}
    """

    return sendAWSQuery(create_event).json()['data']['createEvent']['id']


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
            updateEvent(input: {{id: "{event_id}", name: "{name}", description: "{description}", image: "{image}"}}, condition: null) {{
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
