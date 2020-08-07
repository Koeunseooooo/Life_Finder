from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # 프로필 창 로그인 필요
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Profile
from .forms import RegisterProfileForm,ObjectGoalNumberForm

from .forms import CreateUserForm, CustomAuthenticationForm  # 회원가입
from django.contrib.auth.forms import AuthenticationForm  # 로그인
from django.contrib.auth import login as auth_login  # 로그인

from django.contrib.auth import logout as auth_logout  # 로그아웃


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
            return redirect('create_profile:register')
    elif request.method == 'GET':
        user_form = CreateUserForm()
    return render(request, 'create_profile/signup.html', {
        'user_form': user_form,
    })


def logout(request):
    auth_logout(request)
    return redirect('main:first')


# @login_required  # 로그인 된 사람만 응답하게. 로그인X시 로그인 창 뜸
# def profile(request, pk):
#     user = User.objects.get(pk=pk)  # 프로필의 user
#     profile_info = user.user_profile
#     ctx = {
#         'profile_info': profile_info
#     }
#     return render(request, 'create_profile/profile.html', ctx)
@login_required
def profile_look(request, pk):
    user = User.objects.get(id=pk)
    profile = user.user_profile
    ctx = {
        'profile': profile
    }
    return render(request,'create_profile/profile.html',ctx)

@login_required
def register(request):
    if request.method == 'POST':
        profile_form = RegisterProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            user = request.user
            profile = Profile.objects.create(
                user=user,
                nickname=profile_form.cleaned_data['nickname'],
                photo=profile_form.cleaned_data['photo'],
                age=profile_form.cleaned_data['age'],
                job=profile_form.cleaned_data['job'],
                description=profile_form.cleaned_data['description'],
            )
            return redirect('main:first')
    else:
        profile_form = RegisterProfileForm()

    return render(request, 'create_profile/register.html', {
        'profile_form': profile_form,
    })


def profile_edit(request,pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        profile_form = RegisterProfileForm(request.POST, request.FILES, instance=profile)
        goal_form = ObjectGoalNumberForm(request.POST,instance=profile)
        if profile_form.is_valid():
            # profile = profile_form.save()
            profile_form.save()
            goal_form.save()
        return redirect('create_profile:profile_look', profile.pk)
    else:
        profile_form = RegisterProfileForm(instance=profile)
        goal_form = ObjectGoalNumberForm(instance=profile)
        ctx = {
            'profile_form': profile_form,
            'goal_form': goal_form,
        }
        return render(request,'create_profile/profile_update.html',ctx)
