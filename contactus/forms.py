# sendemail/forms.py
from django import forms


class ContactForm(forms.Form):
    oggetto = forms.CharField(required=True)
    messaggio = forms.CharField(widget=forms.Textarea, required=True)
