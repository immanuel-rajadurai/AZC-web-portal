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
