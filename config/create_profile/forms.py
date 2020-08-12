from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Profile
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple

# class CreateUserForm(UserCreationForm):  # 회원가입폼
#     class Meta:
#         model = User
#         fields = ["username", "password1", "password2"]
#         labels = {"username": "ID"}


class CreateUserForm(UserCreationForm):  # 회원가입 폼
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields['username'].widget.attrs.update({'placeholder': '아이디'})
            self.fields['username'].label = ''
            self.fields['password1'].widget.attrs.update({'placeholder': '비밀번호'})
            self.fields['password1'].label = ''
            self.fields['password2'].widget.attrs.update({'placeholder': '비밀번호 재확인'})
            self.fields['password2'].label = ''

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)

        if commit:
            user.save()
        return user


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
        widgets = {
            'interested': RadioSelect()
            # 'interested': CheckboxSelectMultiple()

        }
        fields = ['nickname', 'photo', 'job', 'description', 'interested']


# class ObjectGoalNumberForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['goal_count']
#         labels = {"goal_count": "목표 개수"}


# class RangeInput(NumberInput):
#     input_type = 'range'


# goal_count = forms.IntegerField(widget=NumberInput(attrs={'type': 'range', 'max': '100', 'min': '0', 'step': '1'}))


from django.forms.widgets import NumberInput


class ObjectGoalNumberForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['goal_count']
        labels = {"goal_count": "목표 개수"}
        widgets = {'goal_count': NumberInput(attrs={'type': 'range', 'max': '100', 'min': '0', 'step': '1'})}

    # scale = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'step': '5', 'min': '-100', 'max': '100', 'id':'myRange'}), required=False)
# forms.IntegerField(widget=NumberInput(attrs={'type':'range', 'step': '2'}))

# class MyForm(ModelForm):
#     ....
#     class Meta:
#
#         model = Application
#         fields = ['amount', 'reason']
#         widgets = {
#             'amount' : RangeInput(attrs={'max': 100000,
#             'min':10000,
#             'step':5000}),
#
#         }
