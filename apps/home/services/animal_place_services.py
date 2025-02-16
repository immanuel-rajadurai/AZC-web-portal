from .services_extras import *


def add_place_to_event(event_id, place_id):
    check_event_place = f"""
        query listEventPlaces {{
            listEventPlaces(filter: {{ eventID: {{eq: "{ event_id }"}} }}) {{
                items {{
                    placeID
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


def add_animal_to_place(animal_id, place_id):
    check_animal_place = f"""
        query listPlaceAnimals {{
            listPlaceAnimals(filter: {{ placeID: {{eq: "{ place_id }"}}, animalID: {{eq: "{ animal_id }"}} }}) {{
                items {{
                    id
                }}
            }}
        }}
    """
    response = sendAWSQuery(check_animal_place)

    if len(response.json()["data"]["listPlaceAnimals"]["items"]) == 0:
        create_animal_place = f"""
            mutation createPlaceAnimal {{
                createPlaceAnimal(input: {{
                    placeID: "{place_id}",
                    animalID: "{animal_id}"}}) {{
                        id
                }}
            }}
        """
        sendAWSQuery(create_animal_place)


def get_animals_linked_to_place(place_id):
    list_place_animals = f"""
        query listPlaceAnimals {{
            listPlaceAnimals(filter: {{ placeID: {{eq: "{ place_id }"}} }}) {{
                items {{
                    animalID
                }}
            }}
        }}
    """

    return sendAWSQuery(list_place_animals).json()["data"]["listPlaceAnimals"]["items"]


def remove_animal_from_place(animal_id, place_id):
    get_relationships = f"""
        query listPlaceAnimals {{
            listPlaceAnimals(filter: {{animalID: {{eq: "{animal_id}"}}, placeID: {{eq: "{place_id}"}}}}) {{
                items {{
                    id
                }}
            }}
        }}
    """

    relationships = sendAWSQuery(get_relationships).json()["data"]["listPlaceAnimals"]["items"]

    for rel in relationships:
        delete_relationship = f"""
            mutation deletePlaceAnimal {{
                deletePlaceAnimal(input: {{id: "{rel['id']}"}}) {{
                    id
                }}
            }}
        """

        sendAWSQuery(delete_relationship)
