from django.test import TestCase

from django.urls import reverse

class register_userTestCase(TestCase):
    def setUp(self):
        self.url = reverse('register')
    
    def test_register_url(self):
        self.assertEqual(self.url, '/register/')
        
    def test_login_is_successful(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_login_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/register.html')
        
    def test_include_necessary_fields(self):
        response = self.client.get(self.url)
        self.assertIn('form', response.context)
        self.assertIn('msg', response.context)
        self.assertIn('success', response.context)