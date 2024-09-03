import requests
import json

API_KEY = 'da2-cppg5ki5c5gwtenwpabd3csahe'
APPSYNC_ENDPOINT = """https://43ey4asyffgypdekr6hrqdu76i.appsync-api.eu-west-2.amazonaws.com/graphql"""

# The headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}

list_events = """
  query ListEvents {
    listEvents {
      items {
        id
        description
        name
        image
      }
    }
  }
"""


def get_events_list():
    list_events = """
        query ListEvents {
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

    print(response.json())

    return response.json()["data"]["listEvents"]["items"]


def create_event(name, description, place_id, image=None, animal_id=None):
    create_event_payload = {
        'query': f"""
            mutation createEvent {{
               createEvent(input: {{id: {id},
                name: "{name},
                description: {description},
                image: {image},
                place_id: {place_id},
                animal_id: {animal_id}}}) {{
                 id
               }}
            }}
      """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(create_event_payload))

    return response.json()


def delete_event(id):
    delete_event_payload = {
        'query': f"""
            mutation deleteEvent {{
               deleteEvent(input: {{id: {id}}}) {{
                 id
               }}
            }}
      """
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(delete_event_payload))

    return response.json()
