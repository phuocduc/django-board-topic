from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class PasswordResetMailTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='coca3', email='coca3@gmail.com' , password='Avatar@123')
        self.response = self.client.post(reverse('password_reset'), {'email': 'coca3@gmail.com'})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('[Django Boards] Please reset your password', self.email.subject)
    
    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url =reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token' : token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('coca3', self.email.body)
        self.assertIn('coca3@gmail.com', self.email.body)

    def test_email_to(self):
        self.assertEqual(['coca3@gmail.com'], self.email.to)