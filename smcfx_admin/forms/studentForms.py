
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentCreateForm(forms.Form):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=False, max_length=150)
    last_name = forms.CharField(required=False, max_length=150)
    is_active = forms.BooleanField(required=False, initial=True, label="Active")

class StudentEditForm(forms.Form):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=False, max_length=150)
    last_name = forms.CharField(required=False, max_length=150)
    is_active = forms.BooleanField(required=False, label="Active")
