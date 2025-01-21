from django import forms
from django.db import models
from Posti.models import Product

class UploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        