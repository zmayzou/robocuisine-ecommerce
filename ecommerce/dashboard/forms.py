from django import forms
from products.models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'category',
            'name',
            'slug',
            'description',
            'price',
            'image',
            'stock',
            'reference',
            'color',
            'is_available'
        ]

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Noir, Rouge, Blanc'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }