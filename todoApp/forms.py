from django import forms

class UserForm(forms.Form):
    city = forms.CharField(max_length=25)
    fullname = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput)