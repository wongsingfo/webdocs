from django import forms
from django.forms import ModelForm, TextInput

from .models import Document, Image


# field docs: https://docs.djangoproject.com/en/3.1/ref/forms/fields/#charfield
# - When the Form is valid, cleaned_data will include a default null value for optional fields.

# https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/#the-save-method
# https://docs.djangoproject.com/en/3.1/ref/forms/widgets/#textinput

class DocumentForm(ModelForm):
    title = forms.CharField(max_length=30, required=False)

    class Meta:
        model = Document
        fields = ('title', 'body')
        widgets = {
            'body': TextInput,
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'
