from .services_extras import *


def get_tags(event_id):
    get_tags = f"""
        query listEventTags {{
            listEventTags(filter: {{ eventID: {{eq: "{ event_id }"}} }}) {{
                items {{
                    tagName
                }}
            }}
        }}
    """

    return sendAWSQuery(get_tags).json()["data"]["listEventTags"]["items"]


def create_tag(event_id, tagName):
    if tagName != "":
        list_event_tags = f"""
            query listEventTags {{
                listEventTags(filter: {{ eventID: {{eq: "{event_id}"}}, tagName: {{eq: "{tagName}" }} }}) {{
                    items {{
                        id
                    }}
                }}
            }}
        """

        response = sendAWSQuery(list_event_tags)

        if not response.json()["data"]["listEventTags"]["items"]:
            create_tag = f"""
                mutation createTag {{
                    createTag(input: {{ name: "{tagName}" }}) {{
                        name
                    }}
                }}
            """

            sendAWSQuery(create_tag)

            create_event_tag = f"""
                mutation createEventTag {{
                    createEventTag(input: {{ eventID: "{event_id}", tagName: "{tagName}" }}) {{
                        id
                    }}
                }}
            """

            sendAWSQuery(create_event_tag)


def delete_tag(event_id, tagName):
    list_event_tags = f"""
        query listEventTags {{
            listEventTags(filter: {{eventID: {{eq: "{event_id}"}}, tagName: {{eq: "{tagName}" }}}}) {{
                items {{
                    id
                }}
            }}
        }}
    """

    for event_tag in sendAWSQuery(list_event_tags).json()["data"]["listEventTags"][
        "items"
    ]:
        delete_event_tags = f"""
            mutation deleteEventTag {{
                deleteEventTag(input: {{id: "{event_tag['id']}"}}) {{
                    id
                }}
            }}
        """

        sendAWSQuery(delete_event_tags)
