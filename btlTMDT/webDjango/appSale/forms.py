from django import forms

class CustomerForm(forms.Form):
    first_name = forms.CharField(max_length=255, required=True, label='First name')
    last_name = forms.CharField(max_length=255, required=True, label='Last name')
    email = forms.EmailField(max_length=255, required=True, label='Email')
    username = forms.CharField(max_length=255, required=True, label='User name')
    password = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput, label='Password')
    repassword = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput, label='Confirm password')
    phone = forms.CharField(max_length=255, required=True, label='Phone number')
    address = forms.CharField(max_length=255, required=True, label='Address')