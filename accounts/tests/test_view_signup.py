from django.urls import reverse
from django.test import TestCase
from django.urls import resolve
from ..views import signup
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ..form import SignupForm
# Create your tests here.
class SingUpTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)
    
    def test_singup_url_resolve_singup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_token_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignupForm)

    def test_forms_input(self):
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="password"', 2)
        
class SingupSuccessTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data={
            'username': 'coca2',
            'password1': 'Avatar@123',
            'password2': 'Avatar@123',
            'email' : 'coca2@gmail.com'
        }

        self.response = self.client.post(url,data)
        self.home_url = reverse('home')

    def test_redirection(self):
        self.assertRedirects(self.response,self.home_url)
    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSingupTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})
    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    def test_user_creation(self):
        self.assertFalse(User.objects.exists())
        