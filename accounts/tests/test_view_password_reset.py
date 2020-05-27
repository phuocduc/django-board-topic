from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core import mail

class PasswordResetTest(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)
    
    def test_view_function(self):
        view = resolve('/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    def test_form_input(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)

class SuccessResetPasswordTest(TestCase):
    def setUp(self):
        email = 'admin@gmail.com'
        User.objects.create_user(username='admina', email=email, password='Avatar@123')
        url = reverse('password_reset')
        self.response = self.client.post(url , {'email': email})

    # def test_redirection(self):
    #     url = reverse('password_reset_done')
    #     self.assertRedirects(self.response,url)
    
    def test_send_password_reset_mail(self):
        
        self.assertEqual(1, len(mail.outbox))

    
class InvalidResetPasswordTest(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'donotexist@email.com'})

    # def test_redirection(self):
    #     url = reverse('password_reset_done')
    #     self.assertRedirects(self.response, url)
    
    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))

class PasswordResetDoneTest(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)
        
    # def test_status_code(self):
    #     self.assertEquals(self.response.status_code, 200)
    
    # def test_view_func(self):
    #     view = resolve('/reset/done/')
    #     self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)

class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='coca5', email='coca5@gmail.com', password='Avatar@123')
        self.uid = urlsafe_base64_decode(force_bytes(user.pk)).decode()
        self.token = default_token_generator.make_token(user)

        url = reverse('password_reset_confirm', kwargs={'uidb64' : self.uid, 'token' : self.token})
        self.response = self.client.get(url, follow=True)

    # def test_status_code(self):
    #     self.assertEquals(self.response.status_code,200)

    # def test_view_function(self):
    #     view = resolve('/reset/{uidb64}/{token}/'.format(uidb64=self.uid, token=self.token))
    #     self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)

    # def test_csrf(self):
    #     self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    # def test_contain_form(self):
    #     form = self.response.context.get('form')
    #     self.assertIsInstance(form, SetPasswordForm)
    
    # def test_form_input(self):
    #     self.assertContains(self.response, '<input ', 3)
    #     self.assertContains(self.response, 'type="password"',2)

class InvalidPasswordResetTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='coca7', email='coca7@gmail.com', password='Avatar@123')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = default_token_generator.make_token(user)

        user.set_password('123@Avatar')
        user.save()

        url = reverse('password_reset_confirm', kwargs={'uidb64' : uid, 'token': token})
        self.response = self.client.get(url)

    # def test_status_code(self):
    #     self.assertEquals(self.response.status_code,200)
    
    # def test_html(self):
    #     password_reset_url = reverse('password_reset')
    #     self.assertContains(self.response, 'invalid password reset link')
    #     self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))

class PasswordResetCompleteTest(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)
    
    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)
    
    def test_view_function(self):
        view = resolve('/reset/complete/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)