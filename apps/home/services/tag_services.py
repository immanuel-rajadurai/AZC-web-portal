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


def create_tag(name):
    create_tag = f"""
        mutation createTag {{
            createTag(input: {{ name: "{name}" }}) {{
                name
            }}
        }}
    """

    sendAWSQuery(create_tag)


def delete_tag(name):
    delete_tag = f"""
        mutation deleteTag {{
            deleteTag(input: {{ name: "{name}" }}) {{
                name
            }}
        }}
    """

    sendAWSQuery(delete_tag)


def delete_tags():
    tags = get_tags_list()
    for tag in tags:
        delete_tag(tag["name"])
