from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .test_helpers import LogInTester

class login_viewTestCase(TestCase, LogInTester):
    def setUp(self):
        self.url = reverse('login')
        
        User.objects.create_user(
            username="johndoe",
            email='johndoe@example.org',
            password='Password123'
        )
        
        self.user = User.objects.get(email='johndoe@example.org')
    
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
        
    def test_msg_is_none(self):
        response = self.client.get(self.url)
        self.assertIs(response.context['msg'], None)
        
    def test_msg_is_not_none(self):
        response = self.client.post(self.url, {'username': '', 'password': ''})
        self.assertEqual(response.context['msg'], 'Error validating the form')
        
    def test_form_is_valid(self):
        response = self.client.post(self.url, {'username': 'test', 'password': 'Password123'})
        self.assertEqual(response.context['msg'], 'Invalid credentials')
        
    def test_valid_credentials(self):
        response = self.client.post(self.url, {'username': 'johndoe', 'password': 'Password123'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self._is_logged_in())