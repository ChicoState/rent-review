from django import forms
from .models import City,Complex, Comments, Posts
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class CityForm(forms.Form):
    city_input = forms.CharField(required=True, label='',
                                 widget=forms.widgets.TextInput(
                                     attrs={ 'style': 'height: 30px; text-align:center; border-radius:10px;', 'id': 'searchBar', 'placeholder': 'City Name', }),
                                 validators=[validators.MinLengthValidator(1)],
                                 max_length=28)

    class Meta:
        model = City
        
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise self.ValidationError('Passwords do not match')
        user.password = self.cleaned_data['password1']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class CommentForm(forms.Form):
    comment_text = forms.CharField(required=True,
        label='',
        widget=forms.widgets.Textarea(attrs={"id":"commentTextArea", "rows":"3" }),
        max_length=1028)
    class Meta:
        model = Comments

class RateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.field.widget.input_type == 'number':
                visible.field.widget.input_type = 'hidden'
    class Meta:
        model = Posts
        exclude = ['user', 'complex', 'date_created']

class CreateComplexForm(forms.Form):
    cityname = forms.CharField(label='City', max_length=28)
    complexName = forms.CharField(label='Complex Name', max_length=64)
    address = forms.CharField(label='Address', max_length=64)
    url = forms.URLField()
    # IRS has lowest zip at 00501
    zipcode = forms.IntegerField(max_value=99999, min_value=501)

    def save(self):
        com = Complex()
        city = City.objects.get(name=self.cleaned_data["cityname"].capitalize())
        com.city_name = city
        com.complex_name = self.cleaned_data["complexName"].capitalize()
        com.address = self.cleaned_data["address"].capitalize()
        com.url = self.cleaned_data["url"]
        com.zipcode = self.cleaned_data["zipcode"]
        com.save()
        return com
