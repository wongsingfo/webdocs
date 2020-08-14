from django import forms
from .models import Document, Image


class DocumentForm(forms.ModelForm):
    title = forms.CharField(max_length=30, required=False)
    body = forms.Textarea()

    class Meta:
        model = Document
        fields = ('title', 'body')


class ImageForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Image
        fields = ('image',)
