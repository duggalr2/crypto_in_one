from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


URL_CHOICES = (
    ('https://medium.com/feed/tag/bitcoin', 'https://medium.com/feed/tag/bitcoin'),
    ('https://medium.com/feed/tag/ethereum', 'https://medium.com/feed/tag/ethereum'),
)


class SignUpForm(UserCreationForm):
    urls = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=URL_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'urls', 'password1', 'password2', )
