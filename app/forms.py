from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from app.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=3, widget=forms.PasswordInput) # textarea


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    #image = forms.ImageField(required=False, label="Upload avatar", widget=forms.FileInput(attrs={"class": "col-9"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username

    def clean(self):
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['password_check']
        if pass1 != pass2:
            raise forms.ValidationError('Passwords do not match')

        if len(pass1) <= 4:
            raise forms.ValidationError('too few characters in the password')
        self.clean_username()

    def save(self):
        self.cleaned_data.pop('password_check')
        if 'username' in self.cleaned_data:
            user = User.objects.create_user(**self.cleaned_data)
            Profile.objects.create(user=user, premium=False)
            return user
        else:
            raise forms.ValidationError('error in form')