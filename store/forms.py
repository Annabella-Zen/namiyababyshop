from django import forms
from django.contrib.auth.models import User
from store.models import UserProfileInfo


class FormUser(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        "class": "form-control", 
        "placeholder": "Username",
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        "class": "form-control", 
        "placeholder": "Email",
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        "class": "form-control", 
        "placeholder": "Password",
    }))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        "class": "form-control", 
        "placeholder": "Confirm Password",
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class FormUserProfileInfo(forms.ModelForm):
    portfolio = forms.URLField(label='Portfolio', required=False, widget=forms.TextInput(attrs={
        "class": "form-control", 
        "placeholder": "Portfolio",
    }))
    image = forms.ImageField(label='Image', required=False, widget=forms.FileInput(attrs={
        "class": "form-control-file"
    }))

    class Meta:
        model = UserProfileInfo
        fields = ('portfolio', 'image')
