from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # 프로필 창 로그인 필요
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Profile
from .forms import RegisterProfileForm, ObjectGoalNumberForm

from .forms import CreateUserForm, CustomAuthenticationForm  # 회원가입
from django.contrib.auth.forms import AuthenticationForm  # 로그인
from django.contrib.auth import login as auth_login  # 로그인

from django.contrib.auth import logout as auth_logout  # 로그아웃


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

    elif request.method == "GET":
        user_form = CreateUserForm()

    return render(request, 'create_profile/signup.html', {
        'user_form': user_form,
    })


@login_required
def goal_get(request):
    user = request.user
    profile = request.user.user_profile
    goal_form = ObjectGoalNumberForm(request.POST)
    if request.method == "POST":
        if goal_form.is_valid():
            goal_count = request.POST['goal_count']
            profile.goal_count = goal_count
            profile.save()
            return redirect('main:first')
    else:
        goal_form = ObjectGoalNumberForm()
    return render(request, 'create_profile/goal_get.html', {'goal_form': goal_form})



def logout(request):
    auth_logout(request)
    return redirect('main:first')


@login_required
def profile_look(request, pk):
    user = User.objects.get(id=pk)
    # profile = request.user.user_profile(id=pk)
    profile = user.user_profile
    ctx = {
        'profile': profile
    }
    return render(request, 'create_profile/profile.html', ctx)


@login_required
def register(request):
    user = request.user
    if request.method == 'POST':
        profile_form = RegisterProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile = Profile.objects.create(
                user=user,
                nickname=profile_form.cleaned_data['nickname'],
                photo=profile_form.cleaned_data['photo'],
                # age=profile_form.cleaned_data['age'],
                # birthday=profile_form.cleaned_data['birthday']
                interested=profile_form.cleaned_data['interested'],
                job=profile_form.cleaned_data['job'],
                description=profile_form.cleaned_data['description'],
            )
            return redirect('create_profile:goal_get')
    else:
        profile_form = RegisterProfileForm()

    return render(request, 'create_profile/register.html', {
        'profile_form': profile_form,
    })





def profile_edit(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        profile_form = RegisterProfileForm(request.POST, request.FILES, instance=profile)
        goal_form = ObjectGoalNumberForm(request.POST, instance=profile)
        if profile_form.is_valid():
            # profile = profile_form.save()
            profile_form.save()
            goal_form.save()
        return redirect('create_profile:profile_look', request.user.pk)
    else:
        profile_form = RegisterProfileForm(instance=profile)
        goal_form = ObjectGoalNumberForm(instance=profile)
        ctx = {
            'profile_form': profile_form,
            'goal_form': goal_form,
            'profile': profile,
        }
        return render(request, 'create_profile/profile_update.html', ctx)

# def profile_edit(request,pk):
#     profile = Profile.objects.get(pk=pk)
#     if request.method == "POST":
#         photo = request.FILES['photo']
#         nickname = request.POST['nickname']
#         age = request.POST['age']
#         job = request.POST['job']
#         description = request.POST['description']
#         goal_count = request.POST['goal_count']
#         return redirect('create_profile:profile_look', request.user.pk)
#     else:
#         profile_form = RegisterProfileForm(instance=profile)
#         goal_form = ObjectGoalNumberForm(instance=profile)
#         ctx = {
#             'profile_form': profile_form,
#             'goal_form': goal_form,
#             'profile':profile,
#         }
#         return render(request,'create_profile/profile_update.html',ctx)
