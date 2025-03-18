import time
from .services_extras import *
from . import tag_services


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


async def create_tag(event_id, tagName):
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
        print(response.json())

        if not response.json()["data"]["listEventTags"]["items"]:
            tag_services.create_tag(tagName)

            create_event_tag = f"""
                mutation createEventTag {{
                    createEventTag(input: {{ eventID: "{event_id}", tagName: "{tagName}" }}) {{
                        id
                    }}
                }}
            """
        
            response2 = await sendAWSQuery(create_event_tag)  
            print(response2.json())


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
