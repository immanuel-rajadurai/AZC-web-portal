import requests
import json
from .api_info import *

headers = {
    'Content-Type': 'application/json',
    'x-api-key': API_KEY
}


def sendAWSQuery(query):
    payload = {
        'query': f"""{query}"""
    }

    return requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))
