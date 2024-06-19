from django import forms
from .models import Collection, Item



class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = [
            'nameUG',
            'descriptionUG',
            'publicUG'
        ]

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'value', 'condition', 'origin', 'description', 'dateOfIssue', 'frontImg',
                  'backImg']

