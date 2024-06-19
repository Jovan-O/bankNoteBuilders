from django import forms
from .models import *


class CreateCollectorAccountForm(forms.ModelForm):
    # class Meta:
    #     model = User
    #     fields = [
    #         'username',
    #     ]

    class Meta:
        model = Collector
        fields = [
            'firstName',
            'lastName',
            'email',
        ]

