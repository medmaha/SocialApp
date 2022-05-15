from users.models import Profile
from django import forms
from django.contrib.auth.models import User


class ProfileFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avater']
