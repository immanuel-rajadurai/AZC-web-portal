from django.test import TestCase
from ...forms import SignUpForm

class SignUpFormTestCase(TestCase):
    def test_form_valid_data(self):
        form = SignUpForm(data={
            'username': 'usertest1',
            'email': 'example@gmail.com',
            'password1': 'tests12345',
            'password2': 'tests12345'
        })
        self.assertTrue(form.is_valid())
        
    def test_form_no_data(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
        
    def test_form_invalid_data(self):
        form = SignUpForm(data={
            'username': '',
            'email': '',
            'password1': '',
            'password2': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
        
    def test_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
        
    def test_fields_have_proper_widgets(self):
        form = SignUpForm()
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Username')
        self.assertEqual(form.fields['username'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Email')
        self.assertEqual(form.fields['email'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['password1'].widget.attrs['placeholder'], 'Password')
        self.assertEqual(form.fields['password1'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['password2'].widget.attrs['placeholder'], 'Password check')
        self.assertEqual(form.fields['password2'].widget.attrs['class'], 'form-control')
        
    def test_fields_have_proper_labels(self):
        form = SignUpForm()
        self.assertEqual(form.fields['username'].label, None)
        self.assertEqual(form.fields['email'].label, None)
        self.assertEqual(form.fields['password1'].label, None)
        self.assertEqual(form.fields['password2'].label, None)
        
    def test_fields_have_proper_help_texts(self):
        form = SignUpForm()
        self.assertEqual(form.fields['username'].help_text, '')
        self.assertEqual(form.fields['email'].help_text, '')
        self.assertEqual(form.fields['password1'].help_text, '')
        self.assertEqual(form.fields['password2'].help_text, '')
        
    def test_fields_have_proper_max_lengths(self):
        form = SignUpForm()
        self.assertEqual(form.fields['username'].max_length, None)
        self.assertEqual(form.fields['email'].max_length, 320)
        self.assertEqual(form.fields['password1'].max_length, None)
        self.assertEqual(form.fields['password2'].max_length, None)
        
    def test_fields_have_proper_required(self):
        form = SignUpForm()
        self.assertTrue(form.fields['username'].required)
        self.assertTrue(form.fields['email'].required)
        self.assertTrue(form.fields['password1'].required)
        self.assertTrue(form.fields['password2'].required)
        
    def test_fields_have_proper_initials(self):
        form = SignUpForm()
        self.assertEqual(form.fields['username'].initial, None)
        self.assertEqual(form.fields['email'].initial, None)
        self.assertEqual(form.fields['password1'].initial, None)
        self.assertEqual(form.fields['password2'].initial, None)
        
    def test_fields_have_proper_form_type(self):
        form = SignUpForm()
        self.assertEqual(form.fields['username'].widget.input_type, 'text')
        self.assertEqual(form.fields['email'].widget.input_type, 'email')
        self.assertEqual(form.fields['password1'].widget.input_type, 'password')
        self.assertEqual(form.fields['password2'].widget.input_type, 'password')