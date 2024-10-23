from .services_extras import *


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

    response = sendAWSQuery(list_tags)
    if response.json()["data"]:
        return response.json()["data"]["listTags"]["items"]

    return []
