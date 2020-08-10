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
from django.contrib.auth.models import User
from create_profile.forms import Profile

from django.utils import timezone
from datetime import datetime, date
from create_profile.models import Profile
from django.contrib.auth.models import User
from django.db.models import Sum, Count


class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'
    context_object_name = 'today_list'  # today_list에는 오늘 등록한 객체들이 포함됨

    def get_queryset(self,**kwargs):
        queryset = {
            'today_list_items': Event.objects.all().filter(profile=self.request.user.user_profile).filter(start_time__date=date.today()),
            'today_list_rating_sum':  Event.objects.all().filter(profile=self.request.user.user_profile).filter(start_time__date=date.today()).aggregate(Sum('rating')).values()
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


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()
    form = EventForm(request.POST or None, instance=instance)
    if "action_add" in request.POST and form.is_valid():
        instance = form.save(commit=False)
        instance.profile = request.user.user_profile
        instance.save()
        return redirect('cal:calendar')
    elif "action_remove" in request.POST:  # 삭제하기 버튼
        instance.delete()
        return redirect('cal:calendar')
    return render(request, 'cal/event.html', {'form': form})


def dash(request):
    # queryset = Event.objects.all()
    # queryset = Event.objects.first()
    # 오늘로 부터 7일전 까지 갖고온다.
    import arrow
    past_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-7).datetime
    future_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).datetime

    select_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-1).datetime
    select_datetime_late = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=0).datetime
    # 왜 -6일까
    events = Event.objects.filter(start_time__gte=past_datetime).filter(start_time__lte=future_datetime).order_by('start_time')
    select_events=Event.objects.filter(start_time__gte=select_datetime).filter(start_time__lte=select_datetime_late).order_by('start_time')
    # future_events = Event.objects.filter(start_time__lte=future_datetime).order_by('start_time')

    count=0
    for select_event in select_events:
        count += 1

    if(count == 0):
        result='no object'
    else:
        result='exists objects'

        # //키야~~~ 이거대로 유알엘 2개  더 파~~





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

    context={
        'events':events,
        'select_events':select_events,
        'result':result,
        # 'mean_value': mean_value,
        # 'count':count
        # 'future_events':future_events
        # 'all_count':all_count
    }
    return render(request, 'cal/index.html', context=context)
