from django.test import TestCase
from ....views.extras import user_views_extras


class TestUserViewsExtras(TestCase):
    def setUp(self):
        self.page_list = user_views_extras.PageList()

    def test_download_opted_in_users(self):
        response = user_views_extras.download_opted_in_users()
        self.assertEqual(response.status_code, 200)

    def test_page_list(self):
        self.assertEqual(self.page_list.lst, [None])
        self.assertEqual(self.page_list.currentPageNum, 0)

    def test_page_list_resets(self):
        self.page_list.add_page("token")
        self.assertEqual(self.page_list.lst, [None, "token"])

        self.page_list.reset()
        self.assertEqual(self.page_list.lst, [None])
        self.assertEqual(self.page_list.currentPageNum, 0)

    def test_page_list_add_page(self):
        self.page_list.add_page("token")
        self.assertEqual(self.page_list.lst, [None, "token"])

    def test_page_list_first_page(self):
        self.assertTrue(self.page_list.is_first_page())

        self.page_list.add_page("token")
        self.assertEqual(self.page_list.lst, [None, "token"])

        self.page_list.forward()
        self.assertFalse(self.page_list.is_first_page())

    def test_page_list_foward(self):
        self.assertEqual(self.page_list.currentPageNum, 0)

        self.page_list.add_page("token")
        self.assertEqual(self.page_list.currentPageNum, 0)

        self.assertEqual(self.page_list.get_forward(), "token")
        self.assertEqual(self.page_list.currentPageNum, 0)

        self.assertEqual(self.page_list.forward(), "token")
        self.assertEqual(self.page_list.currentPageNum, 1)

    def test_page_list_backward(self):
        self.assertEqual(self.page_list.currentPageNum, 0)

        self.page_list.add_page("token")
        self.assertEqual(self.page_list.currentPageNum, 0)
        
        self.page_list.forward()
        self.assertEqual(self.page_list.currentPageNum, 1)

        self.assertEqual(self.page_list.get_backward(), None)
        self.assertEqual(self.page_list.currentPageNum, 1)

        self.assertEqual(self.page_list.backward(), None)
        self.assertEqual(self.page_list.currentPageNum, 0)
