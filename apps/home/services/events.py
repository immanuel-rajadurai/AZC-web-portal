import requests
import json

API_KEY = 'da2-ewwgqtv4a5fkzc4mh7u4sfxkqu'
APPSYNC_ENDPOINT="""https://g4gxobh45jeqrke2ywuday5sgq.appsync-api.eu-west-2.amazonaws.com/graphql"""

# The headers for the HTTP request
headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}

list_events_query="""query ListEvents {
  listEvents {
    items {
      id
      name
      description
      image
    }
  }
}"""

create_event_mutation="""
mutation MyMutation {
  createEvent(input: {name: "Test", image: "https://wildlife.foothillsclusters.com/wp-content/uploads/2023/05/230518-03.jpg", description: "Come and see our eagles as they fly in the sky"}) {
    id
  }
}
"""

delete_event_mutation="""
mutation DeleteEvent {
  deleteEvent(input: {id: "130749d8-3b8c-4fc3-9d0c-1b63c8e4d5aa"}) {
    id
  }
}
"""

def get_events_list():
    
    # The payload for the HTTP request
    payload = {
        'query': list_events_query
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    print(response.json())

    return response.json()["data"]["listEvents"]["items"]

def create_event(name, description, image):
    create_event_mutation = f"""
      mutation MyMutation {{
        createEvent(input: {{name: "{name}", image: "{image}", description: "{description}"}}) {{
          id
        }}
      }}
    """

    payload = {
        'query': create_event_mutation
    }

    # Send the POST request to the AppSync endpoint
    response = requests.post(APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    return response.json()
