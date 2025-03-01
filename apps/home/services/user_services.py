from .services_extras import *


def get_users_list(token):
    PAGE_LIMIT = 10

    if token is None:
        list_users = f"""
            query listUsers {{
                listUsers(limit: {PAGE_LIMIT}) {{
                    items {{
                        email
                        firstName
                        lastName
                        optedIn
                    }}
                    nextToken
                }}
            }}
        """
    else:
        list_users = f"""
            query listUsers {{
                listUsers(limit: {PAGE_LIMIT}, nextToken: "{token}") {{
                    items {{
                        email
                        firstName
                        lastName
                        optedIn
                    }}
                    nextToken
                }}
            }}
        """

    return sendAWSQuery(list_users).json()["data"]["listUsers"]


def get_all_users():
    list_users = """
        query listUsers {
            listUsers {
                items {
                    email
                    firstName
                    lastName
                    optedIn
                }
            }
        }
    """

    return sendAWSQuery(list_users).json()["data"]["listUsers"]["items"]


def get_opted_in_users():
    list_users = f"""
        query listUsers {{
            listUsers(filter: {{ optedIn: {{eq: true }} }}) {{
                items {{
                    email
                    firstName
                    lastName
                    optedIn
                }}
            }}
        }}
    """

    return sendAWSQuery(list_users).json()["data"]["listUsers"]["items"]
