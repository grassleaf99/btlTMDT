from django import forms

class CustomerForm(forms.Form):
    first_name = forms.CharField(max_length=255, required=True, label='First name', widget=forms.TextInput(attrs={'class':'form-control'}))
    mid_name = forms.CharField(max_length=255, required=True, label='Middle name', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=255, required=True, label='Last name', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=255, required=True, label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=255, required=True, label='User name', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=255, required=True, label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    repassword = forms.CharField(max_length=255, required=True, label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    phone = forms.CharField(max_length=255, required=True, label='Phone number', widget=forms.TextInput(attrs={'class':'form-control'}))
    city = forms.CharField(max_length=255, required=True, label='City', widget=forms.TextInput(attrs={'class':'form-control'}))
    district = forms.CharField(max_length=255, required=True, label='District', widget=forms.TextInput(attrs={'class':'form-control'}))
    street = forms.CharField(max_length=255, required=True, label='Street', widget=forms.TextInput(attrs={'class':'form-control'}))
    houseNum = forms.CharField(max_length=255, required=True, label='House Number', widget=forms.TextInput(attrs={'class':'form-control'}))
