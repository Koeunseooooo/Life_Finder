from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
import calendar
from django.utils import timezone
from .models import Event
from .models import *
from .utils import Calendar
from .forms import EventForm
from create_profile.forms import Profile
from django.utils import timezone
from datetime import date,timedelta
from create_profile.models import Profile
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from django.views.generic.dates import DayArchiveView
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse

#setings.py에 보내서 다른 앱의 view에도 today_date라는 변수 넘기기
def give_today_date(request):
    import datetime
    today_date = datetime.date.today().isoformat()
    return {'today_date':today_date}

def send_to_calendar(request):
    import datetime
    today_date = datetime.date.today().isoformat()
    return redirect('cal:calendar',today_date)

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'
    context_object_name = 'today_list'  # today_list에는 오늘 등록한 객체들이 포함됨

    @property
    def date(self):
       return self.kwargs['date']

    def get_queryset(self, **kwargs):
        # date = self.kwargs['date'] or None
        queryset = {
            'today_list_items': Event.objects.all().filter(profile=self.request.user.user_profile).filter(start_time__date=self.kwargs['date']),
            'today_list_rating_sum': Event.objects.all().filter(profile=self.request.user.user_profile).filter(start_time__date=self.kwargs['date']).aggregate(Sum('rating')).values(),
            # 'today_list_items': Event.objects.all().filter(profile=self.request.user.user_profile).filter(start_time__date=date.today()),
            # 'today_list_rating_sum': Event.objects.all().filter(profile=self.request.user.user_profile).filter(start_time__date=date.today()).aggregate(Sum('rating')).values(),
        }
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))

        cal = Calendar(d.year, d.month)
        # issue self.request.user 추가해서 달력에서 다른 사람이 등록한 이벤트 안 보이게 문제 해결
        html_cal = cal.formatmonth(self.request.user, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['today_date'] = self.date
        context['date'] = self.date

        #2020-08-16대신 08월 16일이라고 전달하는 text
        context['date_text'] = self.date[5:7] +'월 ' + self.date[8:] +'일'
        # context['day'] =self.day

        day = self.date
        # day = get_specifiec_date(self.request.GET.get('day', None))
        context['prev_day'] = prev_day(day)
        context['real_today'] = real_today(day)
        context['next_day'] = next_day(day)
        return context

#Prev day버튼 누르면 전날로 이동
def prev_day(day):
    import datetime
    date_time_str = day
    #현재 date_time_str은 str타입이라서 이를 날짜로 바꿔주기
    day_object = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    prev_day = day_object - datetime.timedelta(days=1)
    day = prev_day.isoformat()[:10]
    return day

#TODAY라는 글씨에 오늘 날짜를 전달해주기
def real_today(day):
    import datetime
    today_date = datetime.date.today()
    day = today_date.isoformat()
    return day

#next day버튼 누르면 다음 날로 이동
def next_day(day):
    import datetime
    date_time_str = day
    day_object = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    next_day = day_object + datetime.timedelta(days=1)
    day = next_day.isoformat()[:10]
    return day




def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event_edit(request, event_id):
    import datetime
    today_date = datetime.date.today().isoformat()
    instance = get_object_or_404(Event, pk=event_id)
    form = EventForm(request.POST or None, instance=instance)
    if "action_add" in request.POST and form.is_valid():
        instance = form.save(commit=False)
        instance.profile = request.user.user_profile
        instance.save()
        return redirect('cal:calendar', today_date)
    elif "action_remove" in request.POST:  # 삭제하기 버튼
        instance.delete()
        return redirect('cal:calendar',today_date)
    return render(request, 'cal/event_edit.html', {'form': form, 'today_date': today_date})


def event(request, event_id=None):
    import datetime
    today_date = datetime.date.today().isoformat()
    instance = Event()
    form = EventForm(request.POST or None, instance=instance)
    if "action_add" in request.POST and form.is_valid():
        instance = form.save(commit=False)
        instance.profile = request.user.user_profile
        instance.save()
        return redirect('cal:calendar',today_date)
    return render(request, 'cal/event.html', {'form': form, 'today_date': today_date})



def dash(request):
    queryset = Event.objects.all()
    wanted_goal = Profile.objects.all().values().filter(user=request.user)

    # today=datetime.today().date -> 나중에 이거 형식변환 및 스트링 형변환해서 첫번째 그래프에 낳으면 될듯.
    today=datetime.today()

    # today_date 변수를 넘겨주기
    today_date = today.isoformat()[:10]

    year = today.strftime("%Y")

    one_days_ago = today - timedelta(days=1)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(start_time__date=one_days_ago).aggregate(Sum('rating')).values()


    two_days_ago = one_days_ago - timedelta(days=1)
    two_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(start_time__date=two_days_ago).aggregate(Sum('rating')).values()

    three_days_ago = two_days_ago - timedelta(days=1)
    three_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(start_time__date=three_days_ago).aggregate(Sum('rating')).values()

    four_days_ago = three_days_ago - timedelta(days=1)
    four_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(start_time__date=four_days_ago).aggregate(Sum('rating')).values()

    five_days_ago = four_days_ago - timedelta(days=1)
    five_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(start_time__date=five_days_ago).aggregate(Sum('rating')).values()

    six_days_ago = five_days_ago - timedelta(days=1)
    six_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(start_time__date=six_days_ago).aggregate(Sum('rating')).values()

    seven_days_ago = six_days_ago - timedelta(days=1)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    eight_days_ago = seven_days_ago - timedelta(days=1)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    nine_days_ago = eight_days_ago - timedelta(days=1)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    ten_days_ago = nine_days_ago - timedelta(days=1)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    eleven_days_ago = datetime.today() - timedelta(days=11)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    twelve_days_ago = datetime.today() - timedelta(days=12)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    thirteen_days_ago = datetime.today() - timedelta(days=13)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    fourteen_days_ago = datetime.today() - timedelta(days=14)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    fifteen_days_ago = datetime.today() - timedelta(days=15)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    sixteen_days_ago = datetime.today() - timedelta(days=16)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    seventeen_days_ago = datetime.today() - timedelta(days=17)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    eighteen_days_ago = datetime.today() - timedelta(days=18)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    nineteen_ago = datetime.today() - timedelta(days=19)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    twenty_days_ago = datetime.today() - timedelta(days=20)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    twentyone_days_ago = datetime.today() - timedelta(days=21)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    twentytwo_days_ago = datetime.today() - timedelta(days=22)
    one_days_ago_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(
        start_time__date=one_days_ago).aggregate(Sum('rating')).values()

    twentythree_days_ago = datetime.today() - timedelta(days=23)
    twentyfour_days_ago = datetime.today() - timedelta(days=24)
    twentyfive_days_ago = datetime.today() - timedelta(days=25)
    twentysix_days_ago = datetime.today() - timedelta(days=26)
    twentyseven_days_ago = datetime.today() - timedelta(days=27)
    twentyeight_days_ago = datetime.today() - timedelta(days=28)
    twentynine_days_ago = datetime.today() - timedelta(days=29)
    thirty_daytwenys_ago = datetime.today() - timedelta(days=30)

    pre_one_days_ago = datetime.today() - timedelta(days=31)
    pre_two_days_ago = datetime.today() - timedelta(days=32)
    pre_three_days_ago = datetime.today() - timedelta(days=33)
    pre_four_days_ago = datetime.today() - timedelta(days=34)
    pre_five_days_ago = datetime.today() - timedelta(days=35)
    pre_six_days_ago = datetime.today() - timedelta(days=36)
    pre_seven_days_ago = datetime.today() - timedelta(days=37)
    pre_eight_days_ago = datetime.today() - timedelta(days=38)
    pre_nine_days_ago = datetime.today() - timedelta(days=39)
    pre_ten_days_ago = datetime.today() - timedelta(days=40)

    pre_eleven_days_ago = datetime.today() - timedelta(days=41)
    pre_twelve_days_ago = datetime.today() - timedelta(days=42)
    pre_thirteen_days_ago = datetime.today() - timedelta(days=43)
    pre_fourteen_days_ago = datetime.today() - timedelta(days=44)
    pre_fifteen_days_ago = datetime.today() - timedelta(days=45)
    pre_sixteen_days_ago = datetime.today() - timedelta(days=46)
    pre_seventeen_days_ago = datetime.today() - timedelta(days=47)
    pre_eighteen_days_ago = datetime.today() - timedelta(days=48)
    pre_nineteen_ago = datetime.today() - timedelta(days=49)
    pre_twenty_days_ago = datetime.today() - timedelta(days=50)

    pre_twentyone_days_ago = datetime.today() - timedelta(days=51)
    pre_twentytwo_days_ago = datetime.today() - timedelta(days=52)
    pre_twentythree_days_ago = datetime.today() - timedelta(days=53)
    pre_twentyfour_days_ago = datetime.today() - timedelta(days=54)
    pre_twentyfive_days_ago = datetime.today() - timedelta(days=55)
    pre_twentysix_days_ago = datetime.today() - timedelta(days=56)
    pre_twentyseven_days_ago = datetime.today() - timedelta(days=57)
    pre_twentyeight_days_ago = datetime.today() - timedelta(days=58)
    pre_twentynine_days_ago = datetime.today() - timedelta(days=59)
    pre_thirty_daytwenys_ago = datetime.today() - timedelta(days=60)








    #현재를 기준으로 한달 라이프뱃지들을 가져오는 쿼리문
    one_month_ago = datetime.today() - timedelta(days=30)
    now=Event.objects.all().filter(profile=request.user.user_profile).filter(start_time__gte=one_month_ago).aggregate(Sum('rating')).values()
    for ing in now:
        ing

    #이번달 라이프 일별 뱃지 모으는 쿼리문


    # 운동 선택한 필드만 가져오는 쿼리문
    exercise_field = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='운동').filter(start_time__gte=seven_days_ago)
    # 운동 선택한 필드의 개수만 가져오는 쿼리문
    exercise_field_count = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='운동').filter(start_time__gte=seven_days_ago).count()
    exercise_field_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='운동').filter(start_time__gte=seven_days_ago).aggregate(Sum('rating')).values()
    for value1 in exercise_field_rating:
        value1
    if value1==None:
        value1=0


    # 여행 선택한 필드만 가져오는 쿼리문
    travel_field = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='여행').filter(start_time__gte=seven_days_ago)
    # 여행 선택한 필드의 개수만 가져오는 쿼리문
    travel_field_count = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='여행').filter(start_time__gte=seven_days_ago).count()
    travel_field_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='여행').filter(start_time__gte=seven_days_ago).aggregate(Sum('rating')).values()

    for value2 in travel_field_rating:
        value2
    if value2==None:
        value2=0

    # 기타 선택한 필드만 가져오는 쿼리문
    etc_field = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='기타').filter(start_time__gte=seven_days_ago)
    # 기타 선택한 필드의 개수만 가져오는 쿼리문
    etc_field_count = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='기타').filter(start_time__gte=seven_days_ago).count()
    etc_field_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='기타').filter(start_time__gte=seven_days_ago).aggregate(Sum('rating')).values()
    for value3 in etc_field_rating:
        value3
    if value3==None:
        value3=0

    # 친구/가족과의 시간 선택한 필드만 가져오는 쿼리문
    friend_field =Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='친구/가족과의 시간').filter(start_time__gte=seven_days_ago)
    # 친구/가족과의 시간  선택한 필드의 개수만 가져오는 쿼리문
    friend_field_count =Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='친구/가족과의 시간').filter(start_time__gte=seven_days_ago).count()
    friend_field_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='침구/가족과의 시간').filter(start_time__gte=seven_days_ago).aggregate(Sum('rating')).values()
    for value4 in friend_field_rating:
        value4
    if value4==None:
        value4=0


    # 자기계발 선택한 필드만 가져오는 쿼리문
    self_field = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='자기계발').filter(start_time__gte=seven_days_ago)
    # 자기계발 선택한 필드의 개수만 가져오는 쿼리문
    self_field_count = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='자기계발').filter(start_time__gte=seven_days_ago).count()
    self_field_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='자기계발').filter(start_time__gte=seven_days_ago).aggregate(Sum('rating')).values()
    for value5 in self_field_rating:
        value5
    if value5==None:
        value5=0

    # 취미생활 선택한 필드만 가져오는 쿼리문
    hobby_field = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='취미생활').filter(start_time__gte=seven_days_ago)
    # 취미생활 선택한 필드의 개수만 가져오는 쿼리문
    hobby_field_count = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='취미생활').filter(start_time__gte=seven_days_ago).count()
    hobby_field_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='취미생활').filter(start_time__gte=seven_days_ago).aggregate(Sum('rating')).values()
    for value6 in hobby_field_rating:
        value6
    if value6==None:
        value6=0


    # 여가생활 선택한 필드만 가져오는 쿼리문
    leisure_field = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='여가생활').filter(start_time__gte=seven_days_ago)
    # 여가생활 선택한 필드의 개수만 가져오는 쿼리문
    leisure_field_count = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='여가생활').filter(start_time__gte=seven_days_ago).count()
    leisure_field_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='여가생활').filter(start_time__gte=seven_days_ago).aggregate(Sum('rating')).values()
    for value7 in leisure_field_rating:
        value7
    if value7==None:
        value7=0

    # 일 선택한 필드만 가져오는 쿼리문
    work_field = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='일').filter(start_time__gte=seven_days_ago)
    # 일 선택한 필드의 개수만 가져오는 쿼리문
    work_field_count = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='일').filter(start_time__gte=seven_days_ago).count()
    work_field_rating = Event.objects.all().filter(profile=request.user.user_profile).filter(category__contains='일').filter(start_time__gte=seven_days_ago).aggregate(Sum('rating')).values()
    for value8 in work_field_rating:
        value8
    if value8==None:
        value8=0

    import arrow

    # 모든 라이프기록 객체들 불러올때
    past_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-6).datetime
    future_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=23, minute=59, second=59).shift(days=0).datetime
    events = Event.objects.filter(start_time__gte=past_datetime).filter(profile=request.user.user_profile).filter(start_time__lte=future_datetime).order_by('start_time')

    # -6일째 라이프기록 객체들 불러올때
    one_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-6).datetime
    one_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-5).datetime
    one_select_events  = Event.objects.filter(start_time__gte=one_select_datetime).filter(profile=request.user.user_profile).filter(start_time__lte=one_select_datetime_late).order_by('start_time')


    # -5일째 라이프기록 객체들 불러올 떄
    two_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-5).datetime
    two_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-4).datetime
    two_select_events = Event.objects.filter(start_time__gte=two_select_datetime).filter(profile=request.user.user_profile).filter(start_time__lte=two_select_datetime_late).order_by('start_time')

    # -4일째 라이프기록 객체들 불러올 떄
    three_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-4).datetime
    three_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-3).datetime
    three_select_events = Event.objects.filter(start_time__gte=three_select_datetime).filter(profile=request.user.user_profile).filter(start_time__lte=three_select_datetime_late).order_by('start_time')

    # -3일째 라이프기록 객체들 불러올 떄
    four_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-3).datetime
    four_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-2).datetime
    four_select_events = Event.objects.filter(start_time__gte=four_select_datetime).filter(profile=request.user.user_profile).filter(start_time__lte=four_select_datetime_late).order_by('start_time')

    # -2일째 라이프기록 객체들 불러올 때
    five_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-2).datetime
    five_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-1).datetime
    five_select_events = Event.objects.filter(start_time__gte=five_select_datetime).filter(profile=request.user.user_profile).filter(start_time__lte=five_select_datetime_late).order_by('start_time')

    # -1일째 라이프기록 객체들 불러올 때
    six_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-1).datetime
    six_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=0).datetime
    six_select_events = Event.objects.filter(start_time__gte=six_select_datetime).filter(profile=request.user.user_profile).filter(start_time__lte=six_select_datetime_late).order_by('start_time')

    # today 라이프 기록 객체를 불러올 떄
    seven_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).datetime
    seven_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=1).datetime
    seven_select_events = Event.objects.filter(start_time__gte=seven_select_datetime).filter(profile=request.user.user_profile).filter(start_time__lte=seven_select_datetime_late).order_by('start_time')

    # for seven_select_event


    #graph(1)에 필요한 각 날짜들의 라이프뱃지 'total'값들 + graph(2)에서 뽑아내야하는 '요일'값 list에 넣기
    one=0
    two=0
    three=0
    four=0
    five=0
    six=0
    seven=0
    #one~six는 0에서 6의 값이 랜덤하게 차곡차곡 들어간다.

    one_total = 0
    for one_select_event in one_select_events:
        one_total += one_select_event.rating
        one = one_select_event.start_time.weekday()


    two_total = 0
    for two_select_event in two_select_events:
        two_total += two_select_event.rating
        two= two_select_event.start_time.weekday()

    three_total = 0
    for three_select_event in three_select_events:
        three_total += three_select_event.rating
        three = three_select_event.start_time.weekday()

    four_total = 0
    for four_select_event in four_select_events:
        four_total += four_select_event.rating
        four = four_select_event.start_time.weekday()

    five_total = 0
    for five_select_event in five_select_events:
        five_total += five_select_event.rating
        five = five_select_event.start_time.weekday()

    six_total = 0
    for six_select_event in six_select_events:
        six_total += six_select_event.rating
        six = six_select_event.start_time.weekday()

    seven_total = 0
    for seven_select_event in seven_select_events:
        seven_total += seven_select_event.rating
        seven = seven_select_event.start_time.weekday()

    list=[0,0,0,0,0,0,0]

    for a in range(7):
        if(one==a):
            list[a]=one_total
        if(two==a):
            list[a]=two_total
        if (three == a):
            list[a] = three_total
        if (four == a):
            list[a] = four_total
        if (five == a):
            list[a] = five_total
        if (six == a):
            list[a] = six_total
        if (seven == a):
            list[a] = seven_total

    mon=list[0]
    tue=list[1]
    wed=list[2]
    thur=list[3]
    fri=list[4]
    sat=list[5]
    sun=list[6]

#best1(2번째 항목)를 위해 list 생성 및 for문 돌려서 best 1에 해당하는 날짜랑 event_title(best1한정) 값 불러오기
    # 아직 하지 못한것 : best1 rating값이 best2와 같을땐? 두개를 못 띄우는 상황임.
    third_graphs = [one_total, two_total, three_total, four_total, five_total, six_total, seven_total]
    third_graphs.sort(reverse=True)
    best1 = third_graphs[0]

    select_event_str = []
    best1_start_time = ''

    if best1==one_total :
        for one_select_event in one_select_events:
            select_event_str.append(one_select_event.title)
            # one_best1_str=' '.join(select_event_str)
            # 각기 변수명 각기 다르게 지정해야 할 듯
            best1_start_time = one_select_event.start_time

            # one_best1_start_time = best1_start_time
            # 여기도 똑같아

    if best1 == two_total:
        for two_select_event in two_select_events:
            select_event_str.append(two_select_event.title)
            # two_best1_str = ' '.join(select_event_str)
            best1_start_time = two_select_event.start_time
            # two_best1_start_time = best1_start_time


    if best1 == three_total:
        for three_select_event in three_select_events:
            select_event_str.append(three_select_event.title)
            # three_best1_str = ' '.join(select_event_str)
            best1_start_time = three_select_event.start_time
            # three_best1_start_time = best1_start_time

    if best1 == four_total:
        for four_select_event in four_select_events:
            select_event_str.append(four_select_event.title)
            # four_best1_str = ' '.join(select_event_str)
            best1_start_time = four_select_event.start_time
            # four_best1_start_time = best1_start_time

    if best1 == five_total:
        for five_select_event in five_select_events:
            select_event_str.append(five_select_event.title)
            # five_best1_str = ' '.join(select_event_str)
            best1_start_time = five_select_event.start_time
            # five_best1_start_time = best1_start_time


    if best1 == six_total:
        for six_select_event in six_select_events:
            select_event_str.append(six_select_event.title)
            # six_best1_str = ' '.join(select_event_str)
            best1_start_time = six_select_event.start_time
            # six_best1_start_time = best1_start_time

    if best1 == seven_total:
        for seven_select_event in seven_select_events:
            select_event_str.append(seven_select_event.title)
            # seven_best1_str = ' '.join(select_event_str)
            best1_start_time = seven_select_event.start_time
            # seven_best1_start_time = best1_start_time
            best1_start_time = best1_start_time.date


    # graph3를 위한 파이썬 문법~
    five_count=0
    four_count=0
    three_count=0
    two_count=0
    one_count=0

    for event in events:
        if(event.rating == 5):
            five_count+=1

        if(event.rating == 4):
            four_count+=1

        if(event.rating == 3):
            three_count+=1

        if(event.rating == 2):
            two_count+=1

        if(event.rating == 1):
            one_count+=1

    # queryset = {
    #     'wanted_goal': Profile.objects.all().values().filter(user=request.user)
    # }

    count=0
    for event in events:
        count +=1


    a=arrow.utcnow().day

    context={
        'events':events,

        'one_total':one_total,
        'two_total': two_total,
        'three_total': three_total,
        'four_total': four_total,
        'five_total': five_total,
        'six_total': six_total,
        'seven_total': seven_total,

        'best1':best1,
        'select_event_str' :select_event_str,
        'best1_start_time': best1_start_time,

        'mon':mon,
        'tue':tue,
        'wed':wed,
        'thur':thur,
        'fri':fri,
        'sat':sat,
        'sun':sun,

        'one_count':one_count,
        'two_count':two_count,
        'three_count':three_count,
        'four_count':four_count,
        'five_count':five_count,

        'a':a,
        #a는 뭐야? # 나도 몰라 은서가 넣은 거 아니였어?
        'wanted_goal': wanted_goal,

        # 'queryset':queryset
        # 'one_str':one_str,
        # 'two_str': two_str,
        # 'three_str': three_str,
        # 'four_str': four_str,
        # 'five_str': five_str,
        # # 'seven_str': seven_str,
        # 'one_start_time':one_start_time,

        'exercise_field_count':exercise_field_count,
        'travel_field_count':travel_field_count,
        'etc_field_count':etc_field_count,
        'friend_field_count':friend_field_count,
        'self_field_count': self_field_count,
        'hobby_field_count': hobby_field_count,
        'leisure_field_count': leisure_field_count,
        'work_field_count': work_field_count,

        'value1':value1,
        'value2': value2,
        'value3': value3,
        'value4': value4,
        'value5': value5,
        'value6': value6,
        'value7': value7,
        'value8': value8,

        'ing':ing,

        'today':today,
        'one_days_ago':one_days_ago,
        'two_days_ago':two_days_ago,


        'one_days_ago_rating':one_days_ago_rating,
        'three_days_ago_rating':three_days_ago_rating,

        'year':year,
        'today_date':today_date
    }

    if(count >= 7):
        return render(request, 'cal/index.html', context=context)
    else:
        return render(request, 'cal/less_data.html',context=context)


  # count=0
    # # -3에는 3개의 objects가 있어욤
    # for eventi in events:
    #     if eventi.start_time == select_datetime:
    #         count += 1
    #
    # all_count=count

    # count = 0
    # numsum = 0
    # for event in events:
    #     count += 1
    #     numsum += event.rating
    # mean_value = numsum / (count + 1e-7)
    # 갖고온 이벤트들 레이팅값

def dash_detail(request):
    return render(request, 'cal/dash_detail.html')

