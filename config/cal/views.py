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
from datetime import datetime, date
from create_profile.models import Profile
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required


class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'
    context_object_name = 'today_list'  # today_list에는 오늘 등록한 객체들이 포함됨

    def get_queryset(self, **kwargs):
        # profile_value = Profile.objects.all()
        queryset = {
            'today_list_items': Event.objects.all().filter(profile=self.request.user.user_profile).filter(start_time__date=date.today()),
            'today_list_rating_sum': Event.objects.all().filter(profile=self.request.user.user_profile).filter(start_time__date=date.today()).aggregate(Sum('rating')).values(),
            'wanted_goal': Profile.objects.all().values().filter(user=self.request.user)
            # Event.objects.filter(profile=profile_value)
            # 'wanted_goal': Event.objects.values('profile') 프로필 아이디만 갖고와짐
            # Event.objects.select_related('profile')
            # select_related('profile')
        }

        # CartItem.objects.select_related('product').filter(cart=cart)
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
        return context



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
    instance = get_object_or_404(Event, pk=event_id)
    form = EventForm(request.POST or None, instance=instance)
    if "action_add" in request.POST and form.is_valid():
        instance = form.save(commit=False)
        instance.profile = request.user.user_profile
        instance.save()
        return redirect('cal:calendar')
    elif "action_remove" in request.POST:  # 삭제하기 버튼
        instance.delete()
        return redirect('cal:calendar')
    return render(request, 'cal/event_edit.html', {'form': form})




def event(request, event_id=None):
    instance = Event()
    form = EventForm(request.POST or None, instance=instance)
    if "action_add" in request.POST and form.is_valid():
        instance = form.save(commit=False)
        instance.profile = request.user.user_profile
        instance.save()
        return redirect('cal:calendar')
    # elif "action_remove" in request.POST:  # 삭제하기 버튼
    #     instance.delete()
    #     return redirect('cal:calendar')
    return render(request, 'cal/event.html', {'form': form})


def dash(request):
    queryset = Event.objects.all()
    # queryset = Event.objects.first()
    # 오늘로 부터 7일전 까지 갖고온다.

    wanted_goal = Profile.objects.all().values().filter(user=request.user)
    import arrow

    # 모든 라이프기록 객체들 불러올때
    past_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-6).datetime
    future_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=23, minute=59, second=59).shift(days=0).datetime
    events = Event.objects.filter(start_time__gte=past_datetime).filter(start_time__lte=future_datetime).order_by('start_time')

    # -6일째 라이프기록 객체들 불러올때
    one_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-6).datetime
    one_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-5).datetime
    one_select_events  = Event.objects.filter(start_time__gte=one_select_datetime).filter(start_time__lte=one_select_datetime_late).order_by('start_time')

    one_select_datetime = arrow.utcnow().replace(hour=0, minute=0, second=0).shift(days=-6).datetime
    one_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-5).datetime
    one_select_events = Event.objects.filter(start_time__gte=one_select_datetime).filter(start_time__lte=one_select_datetime_late).order_by('start_time')


    # -5일째 라이프기록 객체들 불러올 떄
    two_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-5).datetime
    two_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-4).datetime
    two_select_events = Event.objects.filter(start_time__gte=two_select_datetime).filter(start_time__lte=two_select_datetime_late).order_by('start_time')

    # -4일째 라이프기록 객체들 불러올 떄
    three_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-4).datetime
    three_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-3).datetime
    three_select_events = Event.objects.filter(start_time__gte=three_select_datetime).filter(start_time__lte=three_select_datetime_late).order_by('start_time')

    # -3일째 라이프기록 객체들 불러올 떄
    four_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-3).datetime
    four_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-2).datetime
    four_select_events = Event.objects.filter(start_time__gte=four_select_datetime).filter(start_time__lte=four_select_datetime_late).order_by('start_time')

    # -2일째 라이프기록 객체들 불러올 때
    five_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-2).datetime
    five_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-1).datetime
    five_select_events = Event.objects.filter(start_time__gte=five_select_datetime).filter(start_time__lte=five_select_datetime_late).order_by('start_time')

    # -1일째 라이프기록 객체들 불러올 때
    six_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-1).datetime
    six_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=0).datetime
    six_select_events = Event.objects.filter(start_time__gte=six_select_datetime).filter(start_time__lte=six_select_datetime_late).order_by('start_time')

    # today 라이프 기록 객체를 불러올 떄
    seven_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).datetime
    seven_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=1).datetime
    seven_select_events = Event.objects.filter(start_time__gte=seven_select_datetime).filter(start_time__lte=seven_select_datetime_late).order_by('start_time')

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
            best1_start_time.isocalendar()
            best1_start_time=best1_start_time
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
        'wanted_goal': wanted_goal,

        # 'queryset':queryset
        # 'one_str':one_str,
        # 'two_str': two_str,
        # 'three_str': three_str,
        # 'four_str': four_str,
        # 'five_str': five_str,
        # # 'seven_str': seven_str,
        # 'one_start_time':one_start_time,
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



