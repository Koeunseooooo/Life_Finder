from django.shortcuts import render

def first(request):
    return render(request, 'main/main.html')



#setings.py에 보내서 다른 앱의 view에도 today_date라는 변수 넘기기
def base(request):
    try:
        user = request.user
        profile_nav = user.user_profile
        return {'profile_nav': profile_nav}
    except Exception:
        i =2
        return {'i': i}

    # return render(request, 'main/base.html',{'profile_nav': profile_nav})
