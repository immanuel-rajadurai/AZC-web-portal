from django.test import TestCase

from django.urls import reverse

class login_viewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('login')
    
    def test_login_url(self):
        self.assertEqual(self.url, '/login/')
        
    def test_login_is_successful(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_login_template(self):
        response = self.client.post(self.url)
        self.assertTemplateUsed(response, 'accounts/login.html')
        
    def test_include_necessary_fields(self):
        response = self.client.get(self.url)
        self.assertIn('form', response.context)
        self.assertIn('msg', response.context)