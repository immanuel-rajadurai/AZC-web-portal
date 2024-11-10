from .services_extras import *


def get_users_list(token):
    # print("nextToken: ", token)

    PAGE_LIMIT = 20

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

    response = sendAWSQuery(list_users)
    # print("response.json(): ", response.json())

    if response.json()["data"]:
        return response.json()["data"]["listUsers"]

    return []
