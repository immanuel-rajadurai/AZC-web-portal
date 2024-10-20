from .services_extras import *


def get_places_list():
    list_places = """
        query listPlaces {
            listPlaces {
                items {
                    id
                    name
                    description
                    isOpen
                    image
                }
            }
        }
    """

    return sendAWSQuery(list_places).json()["data"]["listPlaces"]["items"]


def create_place(name, description, isOpen, image):
    create_place = f"""
        mutation createPlace {{
            createPlace(input: {{name: "{name}", description: "{description}", isOpen: {str(isOpen).lower()}, image: "{image}"}}) {{
                id
            }}
        }}
    """

    sendAWSQuery(create_place)


def delete_attached_relationships(place_id):
    get_relationships = f"""
        query listPlaceAnimals {{
            listPlaceAnimals(filter: {{ placeID: {{eq: "{ place_id }"}} }}) {{
                items {{
                    id
                }}
            }}
        }}
    """

    relationships = sendAWSQuery(get_relationships).json()[
        "data"]["listPlaceAnimals"]["items"]

    for rel in relationships:
        delete_relationships = f"""
            mutation deletePlaceAnimal {{
                deletePlaceAnimal(input: {{id: "{rel['id']}"}}) {{
                    id
                }}
            }}
        """

        sendAWSQuery(delete_relationships)

    get_relationships2 = f"""
        query listEventPlaces {{
            listEventPlaces(filter: {{ placeID: {{eq: "{ place_id }"}} }}) {{
                items {{
                    id
                }}
            }}
        }}
    """

    rel_id = sendAWSQuery(get_relationships2).json()[
        "data"]["listEventPlaces"]["items"]['id']

    delete_relationships2 = {
        'query': f"""
            mutation deleteEventPlace {{
                deleteEventPlace(input: {{id: "{rel_id}"}}) {{
                    id
                }}
            }}
        """
    }

    sendAWSQuery(delete_relationships2)


def delete_place(place_id):
    delete_place = f"""
        mutation deletePlace {{
            deletePlace(input: {{id: "{place_id}"}}) {{
                id
            }}
        }}
    """

    sendAWSQuery(delete_place)
    delete_attached_relationships(place_id)


def edit_place(place_id, name, description, isOpen, image):
    edit_place = f"""
        mutation updatePlace {{
            updatePlace(input: {{id: "{place_id}", name: "{name}", description: "{description}", isOpen: {str(isOpen).lower()}, image: "{image}"}}, condition: null) {{
                id
            }}
        }}
    """

    sendAWSQuery(edit_place)


def get_place(place_id):
    get_place = f"""
        query getPlace {{
            getPlace(id: "{place_id}") {{
                name
                description
                isOpen
                image
            }}
        }}
    """

    return sendAWSQuery(get_place).json()['data']['getPlace']
