from .services_extras import *


def add_place_to_event(event_id, place_id):
    check_event_place_payload = {
        'query': f"""
            query listEventPlaces {{
                listEventPlaces(filter: {{ eventID: {{eq: "{ event_id }"}}, placeID: {{eq: "{ place_id }"}} }}) {{
                    items {{
                        id
                    }}
                }}
            }}
        """
    }
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(check_event_place_payload))
    # print(response.json())

    if len(response.json()["data"]["listEventPlaces"]["items"]) <= 0:
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
            query listEventPlaces {{
                listEventPlaces(filter: {{ eventID: {{eq: "{ event_id }"}} }}) {{
                    items {{
                        placeID
                    }}
                }}
            }}
        """
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    tmp = response.json()["data"]["listEventPlaces"]["items"]

    if tmp:
        # print("listEventPlace: ", tmp)
        return tmp

    return []


def remove_place_from_event(place_id, event_id):
    get_rel_payload = {
        'query': f"""
            query listEventPlaces {{
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
