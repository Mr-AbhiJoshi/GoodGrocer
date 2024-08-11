from django.forms import ModelForm
from .models import Contact
from django.contrib.auth.models import User

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        exclude = ['date']