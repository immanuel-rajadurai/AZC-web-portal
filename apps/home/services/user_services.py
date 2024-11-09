from .services_extras import *


def get_users_list(nextToken=None):
    PAGE_LIMIT = 20

    if nextToken is not None:
        list_users = f"""
            query listUsers {{
                listUsers(limit: 20) {{
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
                listUsers(limit: {PAGE_LIMIT}, nextToken: {nextToken}) {{
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

    response = sendAWSQuery(list_users)
    if response.json()["data"]:
        return response.json()["data"]["listUsers"]

    return []
