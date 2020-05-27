from django.test import TestCase
from ..form import SignupForm

class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = SignupForm()
        excepted = ['username', 'email', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(excepted, actual)