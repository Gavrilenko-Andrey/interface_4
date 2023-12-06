from django import forms
from .models import Product


class AddProductForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'image']


class SearchForm(forms.Form):
    query = forms.CharField()
