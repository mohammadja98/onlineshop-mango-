from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactUser

class ContactForm(forms.ModelForm):
    
    class Meta:
        model = ContactUser
        fields = ("full_name", "email", "message", )
        labels = {
            "full_name": _("Full name"),
            "email": _("Email address"),
            "message": _("Message"),
            }