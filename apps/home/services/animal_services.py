from .services_extras import *
import json


def get_animals_list():
    list_animals = """
        query listAnimals {
            listAnimals {
                items {
                    id
                    name
                    scientificName
                    habitat
                    diet
                    behaviour
                    weightMale
                    weightFemale
                    image
                    conservationStatus
                    funFacts
                }
            }
        }
    """

    return sendAWSQuery(list_animals).json()["data"]["listAnimals"]["items"]


def add_animal(name, scientificName, habitat, diet, behaviour, weightMale, weightFemale, image, conservationStatus, funFacts):
    add_animal = f"""
        mutation createAnimal {{
            createAnimal(input: {{ 
                name: {json.dumps(name)}, 
                scientificName: {json.dumps(scientificName)}, 
                habitat: {json.dumps(habitat)}, 
                diet: {json.dumps(diet)}, 
                behaviour: {json.dumps(behaviour)}, 
                weightMale: {json.dumps(weightMale)}, 
                weightFemale: {json.dumps(weightFemale)}, 
                image: {json.dumps(image)}, 
                conservationStatus: {json.dumps(conservationStatus)}, 
                funFacts: {json.dumps(funFacts)} 
            }}) {{
                id
            }}
        }}
    """

    sendAWSQuery(add_animal)

def get_attached_relationships(animal_id):
    get_relationships = f"""
        query listPlaceAnimals {{
            listPlaceAnimals(filter: {{ animalID: {{eq: "{ animal_id }"}} }}) {{
                items {{
                    id
                }}
            }}
        }}
    """

    return sendAWSQuery(get_relationships).json()["data"]["listPlaceAnimals"]["items"]

def delete_attached_relationships(animal_id):
    get_relationships = f"""
        query listPlaceAnimals {{
            listPlaceAnimals(filter: {{ animalID: {{eq: "{ animal_id }"}} }}) {{
                items {{
                    id
                }}
            }}
        }}
    """

    rels = get_attached_relationships(animal_id)

    for rel in rels:
        delete_relationships = f"""
            mutation deletePlaceAnimal {{
                deletePlaceAnimal(input: {{id: "{rel['id']}"}}) {{
                    id
                }}
            }}
        """

        sendAWSQuery(delete_relationships)


def remove_animal(id):
    remove_animal = f"""
        mutation deleteAnimal {{
            deleteAnimal(input: {{id: "{id}"}}) {{
                id
            }}
        }}
    """

    sendAWSQuery(remove_animal)
    delete_attached_relationships(id)


def edit_animal(
    animal_id,
    name,
    scientificName,
    habitat,
    diet,
    behaviour,
    weightMale,
    weightFemale,
    image,
    conservationStatus,
    funFacts,
):
    edit_animal = f"""
        mutation updateAnimal {{
            updateAnimal(input: {{ 
                id: "{animal_id}", 
                name: "{name}", 
                scientificName: "{scientificName}", 
                habitat: "{habitat}", 
                diet: "{diet}", 
                behaviour: "{behaviour}", 
                weightMale: "{weightMale}", 
                weightFemale: "{weightFemale}", 
                image: "{image}", 
                conservationStatus: "{conservationStatus}", 
                funFacts: "{funFacts}" 
            }}, condition: null) {{
                id
            }}
        }}
    """

    sendAWSQuery(edit_animal)


def get_animal(id):
    get_animal = f"""
        query getAnimal {{
            getAnimal(id: "{id}") {{
                name
                image
                scientificName
                habitat
                diet
                behaviour
                weightMale
                weightFemale
                image
                conservationStatus
                funFacts
            }}
        }}
    """

    return sendAWSQuery(get_animal).json()["data"]["getAnimal"]
