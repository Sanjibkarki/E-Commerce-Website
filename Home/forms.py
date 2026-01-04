from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'Name',
            'Description',
            'Image',
            'Price',
            'Quantity',
            'category',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # small UI niceties
        # textarea rows
        if 'Description' in self.fields:
            self.fields['Description'].widget.attrs.update({'rows': 4, 'class': 'form-control'})

        # add bootstrap classes to other widgets
        for fname in ('Name', 'Price', 'Quantity', 'category'):
            if fname in self.fields:
                self.fields[fname].widget.attrs.update({'class': 'form-control'})

        # file input styling
        if 'Image' in self.fields:
            self.fields['Image'].widget.attrs.update({'class': 'form-control-file'})
