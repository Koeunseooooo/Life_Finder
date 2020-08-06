from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class CreateUserForm(UserCreationForm):  # 회원가입폼
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        labels = {"username": "ID"}



class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='아이디',
    )
    password = forms.CharField(
        label= "비밀번호",
        strip=False,
        widget=forms.PasswordInput,
    )