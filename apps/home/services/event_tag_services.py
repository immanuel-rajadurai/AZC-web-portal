from .services_extras import *


def get_tags(event_id):
    payload = {
        'query': f"""
            query listEventTags {{
                listEventTags(filter: {{ eventID: {{eq: "{ event_id }"}} }}) {{
                    items {{
                        tagName
                    }}
                }}
            }}
        """
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))

    tmp = response.json()["data"]["listEventTags"]["items"]

    if tmp:
        # print("listEventTags: ", tmp)
        return tmp

    return []


def create_tag(event_id, tagName):
    if tagName != "":
        payload = {
            'query': f"""
                query listEventTags {{
                    listEventTags(filter: {{ eventID: {{eq: "{event_id}"}}, tagName: {{eq: "{tagName}" }} }}) {{
                        items {{
                            id
                        }}
                    }}
                }}
            """
        }

        response = requests.post(
            APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload))
        # print(response.json())

        if not response.json()["data"]['listEventTags']['items']:
            payload2 = {
                'query': f"""
                    mutation createTag {{
                        createTag(input: {{ name: "{tagName}" }}) {{
                            name
                        }}
                    }}
                """
            }

            response2 = requests.post(
                APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload2))
            # print(response2.json())

            payload3 = {
                'query': f"""
                    mutation createEventTag {{
                        createEventTag(input: {{ eventID: "{event_id}", tagName: "{tagName}" }}) {{
                            id
                        }}
                    }}
                """
            }

            response3 = requests.post(
                APPSYNC_ENDPOINT, headers=headers, data=json.dumps(payload3))
            # print(response3.json())


def delete_tag(event_id, tagName):
    get_payload = {
        'query': f"""
            query listEventTags {{
                listEventTags(filter: {{eventID: {{eq: "{event_id}"}}, tagName: {{eq: "{tagName}" }}}}) {{
                    items {{
                        id
                    }}
                }}
            }}
        """
    }

    response = requests.post(
        APPSYNC_ENDPOINT, headers=headers, data=json.dumps(get_payload))
    # print("response.json():", response.json())

    # if (response.json()["data"]["listEventTags"]["items"])
    event_tags = response.json()["data"]["listEventTags"]["items"]

    for event_tag in event_tags:
        deletion_payload = {
            'query': f"""
                    mutation deleteEventTag {{
                        deleteEventTag(input: {{id: "{event_tag['id']}"}}) {{
                            id
                        }}
                    }}
                """
        }

        response2 = requests.post(
            APPSYNC_ENDPOINT, headers=headers, data=json.dumps(deletion_payload))
        # print("response2.json(): ", response2.json())
