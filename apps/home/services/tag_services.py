import requests
import json
from .api_info import *

headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}


def get_tags_list():
    list_tags = """
        query listTags {
            listTags {
                items {
                    name
                }
            }
        }
    """

    payload = {
        'query': list_tags
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    # print(response.json())
    if response.json()["data"]:
        return response.json()["data"]["listTags"]["items"]

    return []
