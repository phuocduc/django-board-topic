from django import forms
from ..templatetags.form_tags import field_type, input_class

from django.test import TestCase

class ExampleForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        fields = {'name' , 'password'}

class FieldTypeTests(TestCase):
    def test_fields_widget_type(self):
        form = ExampleForm()
        self.assertEquals('TextInput', field_type(form['name']))
        self.assertEquals('PasswordInput', field_type(form['password']))

class InputClassTest(TestCase):
    def test_unbound_field_initial_state(self):
        form = ExampleForm()
        self.assertEquals('form-control ', input_class(form['name']))
    
    def test_valid_bound_field(self):
        form = ExampleForm({'name' : 'admin' , 'password' : 'Avatar@123'})
        self.assertEquals('form-control is-valid', input_class(form['name']))
        self.assertEquals('form-control ', input_class(form['password']))

    def test_invalid_bound_field(self):
        form = ExampleForm({'name': '', 'password': 'Avatar@123'})
        self.assertEquals('form-control is-invalid', input_class(form['name']))