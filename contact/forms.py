# from django.forms import ModelForm
from .models import Contact
from django import forms


# class ContactForm(ModelForm):
#     class Meta:
#         model = Contact
#         fields = '__all__'


class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=150, label="Name", widget=forms.TextInput(attrs={
        'class': 'form-control fh5co_contact_text_box',
        'placeholder': 'Enter Your Name',
        'required': 'required',
    }))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control fh5co_contact_text_box',
        'placeholder': 'Email',
        'required': 'required',
    }))
    subject = forms.CharField(max_length=264, label="Subject", widget=forms.TextInput(attrs={
        'class': 'form-control fh5co_contact_text_box',
        'placeholder': 'Subject',
        'required': 'required',
    }))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={
        'class': 'form-control fh5co_contacts_message',
        'placeholder': 'Message',
        'required': 'required',
    }))

    class Meta:
        model = Contact
        fields = '__all__'
