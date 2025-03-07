from django.test import TestCase
from ....views.extras import user_views_extras


class TestUserViewsExtras(TestCase):
    def setUp(self):
        self.page_list = user_views_extras.PageList()

    def test_download_opted_in_users(self):
        response = user_views_extras.download_opted_in_users()
        self.assertEqual(response.status_code, 200)

    def test_page_list(self):
        self.assertEqual(self.page_list.__lst, [None])
        self.assertEqual(self.page_list.__currentPageNum, 0)

    def test_page_list_resets(self):
        self.page_list.add_page("token")
        self.assertEqual(self.page_list.__lst, [None, "token"])

        self.page_list.reset()
        self.assertEqual(self.page_list.__lst, [None])
        self.assertEqual(self.page_list.__currentPageNum, 0)

    def test_page_list_add_page(self):
        self.page_list.add_page("token")
        self.assertEqual(self.page_list.__lst, [None, "token"])

    def test_page_list_first_page(self):
        self.assertTrue(self.page_list.is_first_page())

        self.page_list.next_page()
        self.assertFalse(self.page_list.is_first_page())

    def test_page_list_next_page(self):
        self.page_list.add_page("token")
        self.assertEqual(self.page_list.next_page(), "token")

    def test_page_list_previous_page(self):
        self.page_list.add_page("token")
        self.page_list.next_page()
        self.assertEqual(self.page_list.previous_page(), "token")

        self.page_list.previous_page()
        self.assertEqual(self.page_list.previous_page(), None)
