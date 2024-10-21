from .services_extras import *


def add_place_to_event(event_id, place_id):
    check_event_place = f"""
        query listEventPlaces {{
            listEventPlaces(filter: {{ eventID: {{eq: "{ event_id }"}}, placeID: {{eq: "{ place_id }"}} }}) {{
                items {{
                    id
                }}
            }}
        }}
    """

    response = sendAWSQuery(check_event_place)

    if len(response.json()["data"]["listEventPlaces"]["items"]) <= 0:
        create_event_place = f"""
            mutation createEventPlace {{
                createEventPlace(input: {{
                    placeID: "{place_id}",
                    eventID: "{event_id}"}}) {{
                        id
                }}
            }}
        """
        sendAWSQuery(create_event_place)


def get_places_linked_to_event(event_id):
    list_event_places = f"""
        query listEventPlaces {{
            listEventPlaces(filter: {{ eventID: {{eq: "{ event_id }"}} }}) {{
                items {{
                    placeID
                }}
            }}
        }}
    """

    return sendAWSQuery(list_event_places).json()[
        "data"]["listEventPlaces"]["items"]


def remove_place_from_event(place_id, event_id):
    get_relationships = f"""
        query listEventPlaces {{
            listEventPlaces(filter: {{eventID: {{eq: "{event_id}"}}, placeID: {{eq: "{place_id}"}}}}) {{
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
