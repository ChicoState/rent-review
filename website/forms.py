from django import forms
from .models import Cities, Comments, Posts
from django.core import validators
from django.contrib.auth.models import User

class CityForm(forms.Form):
    city_input = forms.CharField(required=True,
        label='',
        widget=forms.widgets.Textarea(attrs={'style': 'width: 80%', 'style': 'height: 30px', 'id': 'searchBar', 'placeholder':'City Name', }),
        validators=[validators.MinLengthValidator(1)],
        max_length=28)
    class Meta:
        model = Cities
        
class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
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

class CommentForm(forms.Form):
    comment_text = forms.CharField(required=True,
        label='',
        widget=forms.widgets.Textarea(attrs={"id":"commentTextArea", "rows":"3" }),
        max_length=1028)
    class Meta:
        model = Comments

class RateForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ['user', 'complex', 'date_created']
