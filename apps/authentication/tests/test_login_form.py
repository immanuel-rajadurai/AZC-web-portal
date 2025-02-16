from unittest import TestCase
from ..forms import LoginForm

class LoginFormTestCase(TestCase):
    def test_form_valid_data(self):
        form = LoginForm(data={
            'username': 'test',
            'password': 'test'
        })
        self.assertTrue(form.is_valid())
        
    def test_form_no_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        
    def test_form_invalid_data(self):
        form = LoginForm(data={
            'username': '',
            'password': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
    
    def test_form_has_necessary_fields(self):
        form = LoginForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        
    def test_form_fields_have_proper_widgets(self):
        form = LoginForm()
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Username')
        self.assertEqual(form.fields['username'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['password'].widget.attrs['placeholder'], 'Password')
        self.assertEqual(form.fields['password'].widget.attrs['class'], 'form-control')
        
    def test_form_fields_have_proper_labels(self):
        form = LoginForm()
        self.assertEqual(form.fields['username'].label, None)
        self.assertEqual(form.fields['password'].label, None)
        
    def test_form_fields_have_proper_help_texts(self):
        form = LoginForm()
        self.assertEqual(form.fields['username'].help_text, '')
        self.assertEqual(form.fields['password'].help_text, '')
        
    def test_form_fields_have_proper_max_lengths(self):
        form = LoginForm()
        self.assertEqual(form.fields['username'].max_length, None)
        self.assertEqual(form.fields['password'].max_length, None)
        
    def test_form_fields_have_proper_required(self):
        form = LoginForm()
        self.assertTrue(form.fields['username'].required)
        self.assertTrue(form.fields['password'].required)
    
    def test_form_fields_have_proper_initials(self):
        form = LoginForm()
        self.assertEqual(form.fields['username'].initial, None)
        self.assertEqual(form.fields['password'].initial, None)
        
    def test_form_has_proper_form_type(self):
        form = LoginForm()
        self.assertEqual(form.fields['username'].widget.input_type, 'text')
        self.assertEqual(form.fields['password'].widget.input_type, 'password')
    