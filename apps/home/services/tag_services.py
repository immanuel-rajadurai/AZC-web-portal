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

    return sendAWSQuery(list_tags).json()["data"]["listTags"]["items"]
