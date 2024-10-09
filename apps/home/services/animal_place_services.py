import requests
import json
from .api_info import *

# The headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}


def add_place_to_event(event_id, place_id):
    check_event_place_payload = {
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
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(check_event_place_payload))

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


def add_animal_to_place(animal_id, place_id):
    check_animal_place_payload = {
        'query': f"""
            query listPlaceAnimal {{
                listPlaceAnimals(filter: {{ placeID: {{eq: "{ place_id }"}}, animalID: {{eq: "{ animal_id }"}} }}) {{
                    items {{
                        id
                    }}
                }}
            }}
        """
    }
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(check_animal_place_payload))
    # print(response.json())

    if len(response.json()["data"]["listPlaceAnimals"]["items"]) <= 0:
        create_animal_place_payload = {
            'query': f"""
                mutation createPlaceAnimal {{
                    createPlaceAnimal(input: {{
                        placeID: "{place_id}",
                        animalID: "{animal_id}"}}) {{
                            id
                    }}
                }}
            """
        }
        requests.post(
            APPSYNC_ENDPOINT, headers=headers, data=json.dumps(create_animal_place_payload))


def get_animals_linked_to_place(place_id):
    payload = {
        'query': f"""
            query listPlaceAnimal {{
                listPlaceAnimals(filter: {{ placeID: {{eq: "{ place_id }"}} }}) {{
                    items {{
                        animalID
                    }}
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    tmp = response.json()["data"]["listPlaceAnimals"]["items"]
    # print("tmp: ", tmp)

    if tmp:
        # print("listPlaceAnimals: ", tmp)
        return tmp

    return None


def remove_animal_from_place(animal_id, place_id):
    get_rel_payload = {
        'query': f"""
            query ListPlaceAnimalsFilter {{
                listPlaceAnimals(filter: {{animalID: {{eq: "{animal_id}"}}, placeID: {{eq: "{place_id}"}}}}) {{
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

    rel_id = response.json()["data"]["listPlaceAnimals"]["items"][0]['id']
    # print("rel_id: ", rel_id)

    delete_rel_payload = {
        'query': f"""
            mutation deletePlaceAnimal {{
                deletePlaceAnimal(input: {{id: "{rel_id}"}}) {{
                    id
                }}
            }}
        """
    }

    # Send the POST request to the AppSync endpoint
    response2 = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_rel_payload))
    # print("response2.json(): ", response2.json())
