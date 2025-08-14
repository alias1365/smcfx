# smcfx_admin/forms.py
from django import forms

class StudentCreateForm(forms.Form):
    email = forms.EmailField(
        required=True, label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control", "placeholder": "student@example.com"
        })
    )
    first_name = forms.CharField(
        required=False, max_length=150, label="First name",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        required=False, max_length=150, label="Last name",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    is_active = forms.BooleanField(
        required=False, initial=True, label="Active",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

class StudentEditForm(forms.Form):
    email = forms.EmailField(
        required=True, label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control", "placeholder": "student@example.com"
        })
    )
    first_name = forms.CharField(
        required=False, max_length=150, label="First name",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        required=False, max_length=150, label="Last name",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    is_active = forms.BooleanField(
        required=False, label="Active",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

class StudentDeleteForm(forms.Form):
    """
    بدون صفحه‌ی جدا: همین فرم را کنار Edit نشان می‌دهیم.
    برای اطمینان، یک تیک تایید می‌گیریم.
    """
    confirm = forms.BooleanField(
        required=True, label="I confirm deleting this student",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
