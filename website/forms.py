from django import forms
from .models import Cities
from django.core import validators

class CityForm(forms.Form):
    city_input = forms.CharField(required=True,
        label='',
        widget=forms.widgets.Textarea(attrs={'style': 'width: 80%', 'style': 'height: 30px', 'id': 'searchBar', 'placeholder':'City Name', }),
        validators=[validators.MinLengthValidator(1)],
        max_length=28)
    class Meta:
        model = Cities
