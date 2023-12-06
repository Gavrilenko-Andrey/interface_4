from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserRegistrationForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, min_length=2)
    first_name = forms.CharField(required=False, max_length=50)
    email = forms.CharField(required=True, widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    # class Meta:
    #     model = get_user_model()
    #     fields = ['username', 'first_name']

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).count() > 0:
            raise forms.ValidationError('Пользователь с данным псевдонимом уже зарегистрирован')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).count() > 0:
            raise forms.ValidationError('Пользователь с данной электронной почтой уже зарегистрирован')
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return cd['password2']


class UserEditForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return cd['password2']

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if get_user_model().objects.filter(email=email).count() > 0:
    #         raise forms.ValidationError('Пользователь с данной электронной почтой уже зарегистрирован')
    #     return email


class ProfileEditForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput, required=False)

    class Meta:
        model = Profile
        fields = ['photo']
