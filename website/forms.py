from django import forms
from .models import Cities
from django.core import validators
from django.contrib.auth.models import User


class CityForm(forms.Form):
    city_input = forms.CharField(required=True,
                                 label='',
                                 widget=forms.widgets.Textarea(
                                     attrs={'style': 'width: 80%', 'style': 'height: 30px', 'id': 'searchBar', 'placeholder': 'City Name', }),
                                 validators=[validators.MinLengthValidator(1)],
                                 max_length=28)

    class Meta:
        model = Cities


class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        help_texts = {
            'username': None
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class CreateComplexForm(forms.Form):
    cityname = forms.CharField(label='City', max_length=28)
    complexName = forms.CharField(label='Complex Name', max_length=64)
    address = forms.CharField(label='Address', max_length=64)
    url = forms.URLField()
    zipcode = forms.IntegerField()

    def save(self):
        com = Cities()
        com.name = self.cleaned_data["cityname"]
        com.complex_name = self.cleaned_data["complexName"]
        com.address = self.cleaned_data["address"]
        com.url = self.cleaned_data["url"]
        com.zipcode = self.cleaned_data["zipcode"]
        com.save()
        return com
