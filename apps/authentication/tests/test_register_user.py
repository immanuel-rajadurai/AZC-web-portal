from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import User

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
        
    def test_form_is_invalid(self):
        response = self.client.post(self.url, {'username': '', 'password1': ''})
        self.assertEqual(response.context['msg'], 'Form is not valid')
        
    def test_form_is_invalid(self):
        response = self.client.post(self.url, {'username': 'janedoe', 'email': 'janedoe@example.org', 'password1': 'testingpassword123', 'password2': 'testingpassword123'})
        self.assertEqual(response.context['msg'], """User created - please <a href="/login">login</a>.""")
        self.assertEquals(response.context['success'], True)
        
        user = User.objects.get(username='janedoe')
        self.assertIsNotNone(user)
        
        self.assertIs(user.is_active, True)
        self.assertIsNotNone(user.check_password('testingpassword123'))
        self.assertEqual(user.email, 'janedoe@example.org')