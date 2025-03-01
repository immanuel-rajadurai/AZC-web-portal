from django.test import TestCase
from ...services import user_services

from ...services.services_extras import sendAWSQuery
import json


class UserServicesTestCase(TestCase):
    def create_user(self):
        create_user = f"""
            mutation createUser {{
                createUser(input: {{ 
                    email: {json.dumps("test@example.org")},
                    firstName: {json.dumps("Damon")},
                    lastName: {json.dumps("Salvotore")},
                    optedIn: {json.dumps(False)}
                }}) {{
                    email
                }}
            }}
        """

        sendAWSQuery(create_user).json()

        create_user_optedIn = f"""
            mutation createUser {{
                createUser(input: {{ 
                    email: {json.dumps("test2@example.org")},
                    firstName: {json.dumps("Damon")},
                    lastName: {json.dumps("Salvotore")},
                    optedIn: {json.dumps(True)}
                }}) {{
                    email
                }}
            }}
        """

        sendAWSQuery(create_user_optedIn).json()

    def delete_user(self):
        users = user_services.get_all_users()

        user = next(
            (user for user in users if user["email"] == "test@example.org"), None
        )
        delete_user = f"""
            mutation deleteUser {{
                deleteUser(input: {{ email: "{user['email']}" }}) {{
                    email
                }}
            }}
        """

        sendAWSQuery(delete_user)

        user2 = next(
            (user2 for user2 in users if user2["email"] == "test2@example.org"), None
        )
        delete_user2 = f"""
            mutation deleteUser {{
                deleteUser(input: {{ email: "{user2['email']}" }}) {{
                    email
                }}
            }}
        """

        sendAWSQuery(delete_user2)

    def setUp(self):
        self.create_user()

    def tearDown(self):
        self.delete_user()

    def test_get_users_list(self):
        users = user_services.get_users_list(None)
        self.assertNotEqual(len(users), [])

    def test_get_users_optedIn(self):
        users = user_services.get_opted_in_users()
        for user in users:
            self.assertTrue(user["optedIn"])

        all_users = user_services.get_all_users()
        opted_in_users = []
        for user in all_users:
            if user["optedIn"]:
                opted_in_users.append(user)

        self.assertEqual(
            sorted(users, key=lambda x: x["email"]),
            sorted(opted_in_users, key=lambda x: x["email"]),
        )
