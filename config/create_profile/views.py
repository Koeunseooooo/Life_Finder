from django.shortcuts import render, redirect


from .forms import CreateUserForm, CustomAuthenticationForm #회원가입
from django.contrib.auth.forms import AuthenticationForm #로그인
from django.contrib.auth import login as auth_login #로그인

from django.contrib.auth import logout as auth_logout #로그아웃
# Create your views here.
# def page(request):
#     return render(request, 'create_profile/page.html')

def login(request):
    if request.method == 'POST':
        login_form = CustomAuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
        return redirect('main:first')

    else:
        login_form = CustomAuthenticationForm()

    return render(request, 'create_profile/login.html', {'login_form': login_form})


def signup(request):
    if request.method == "POST":
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)  # 로그인 처리
            return redirect('main:first')
    elif request.method == 'GET':
        user_form = CreateUserForm()
    return render(request, 'create_profile/signup.html', {
        'user_form': user_form,
    })


def logout(request):
    auth_logout(request)
    return redirect('main:first')
