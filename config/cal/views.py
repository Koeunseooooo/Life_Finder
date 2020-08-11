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
        queryset = {
            'today_list_items': Event.objects.all().filter(profile=self.request.user.user_profile).filter(start_time__date=date.today()),
            'today_list_rating_sum': Event.objects.all().filter(profile=self.request.user.user_profile).filter(start_time__date=date.today()).aggregate(Sum('rating')).values()
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

    # if event_id:
    #     instance = get_object_or_404(Event, pk=event_id)
    # else:
    #     instance = Event()
    # form = EventForm(request.POST or None, instance=instance)
    # if "action_add" in request.POST and form.is_valid():
    #     instance = form.save(commit=False)
    #     instance.profile = request.user.user_profile
    #     instance.save()
    #     return redirect('cal:calendar')
    # elif "action_remove" in request.POST:  # 삭제하기 버튼
    #     instance.delete()
    #     return redirect('cal:calendar')
    # return render(request, 'cal/event.html', {'form': form})

def dash(request):
    # queryset = Event.objects.all()
    # queryset = Event.objects.first()
    # 오늘로 부터 7일전 까지 갖고온다.
    import arrow

    past_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-6).datetime
    future_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=23, minute=59, second=59).shift(days=0).datetime
    events = Event.objects.filter(start_time__gte=past_datetime).filter(start_time__lte=future_datetime).order_by('start_time')


    # one_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-6).datetime
    # one_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-5).datetime
    # one_select_events=Event.objects.filter(start_time__gte=one_select_datetime).filter(start_time__lte=one_select_datetime_late).order_by('start_time')
    #
    # two_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-5).datetime
    # two_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-4).datetime
    # two_select_events = Event.objects.filter(start_time__gte=two_select_datetime).filter(start_time__lte=two_select_datetime_late).order_by('start_time')
    #
    # three_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-4).datetime
    # three_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-3).datetime
    # three_select_events = Event.objects.filter(start_time__gte=three_select_datetime).filter(start_time__lte=three_select_datetime_late).order_by('start_time')
    #
    # four_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-3).datetime
    # four_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-2).datetime
    # four_select_events = Event.objects.filter(start_time__gte=four_select_datetime).filter(start_time__lte=four_select_datetime_late).order_by('start_time')
    #
    # five_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-2).datetime
    # five_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-1).datetime
    # five_select_events = Event.objects.filter(start_time__gte=five_select_datetime).filter(start_time__lte=five_select_datetime_late).order_by('start_time')
    #
    # six_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-1).datetime
    # six_select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=0).datetime
    # six_select_events = Event.objects.filter(start_time__gte=six_select_datetime).filter(start_time__lte=six_select_datetime_late).order_by('start_time')
    #
    # seven_select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).datetime
    # seven_select_events = Event.objects.filter(start_time__gte=seven_select_datetime).order_by('start_time')
    #
    # count=0
    # for one_select_event in one_select_events:
    #     count+=1
    #     break
    #
    # for two_select_event in two_select_events:
    #     count+=1
    #     break
    #
    # for three_select_event in three_select_events:
    #     count+=1
    #     break
    #
    # for four_select_event in four_select_events:
    #     count+=1
    #     break
    #
    # for five_select_event in five_select_events:
    #     count+=1
    #     break
    #
    # for six_select_event in six_select_events:
    #     count+=1
    #     break
    #
    # for seven_select_event in seven_select_events:
    #     count+=1
    #     break

    count=0

    for event in events:
        count +=1

    context={
        'events':events,
        # 'one_select_events':one_select_events,
        # 'two_select_events': two_select_events,
        # 'three_select_events': three_select_events,
        # 'four_select_events': four_select_events,
        # 'five_select_events': five_select_events,
        # 'six_select_events': six_select_events,
        # 'seven_select_events': seven_select_events,
        'count':count,
        # 'mean_value': mean_value,
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
