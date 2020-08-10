from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Profile


class CreateUserForm(UserCreationForm):  # 회원가입폼
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        labels = {"username": "ID"}


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='',
    )
    password = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput,
    )


class RegisterProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'photo', 'age', 'job', 'description']


class ObjectGoalNumberForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['goal_count']
