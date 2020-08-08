from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
import calendar
from django.db.models import Q

from .models import *
from .utils import Calendar
from .forms import EventForm

# def index(request):
#     queryset = Article.objects.all()
#     context = {
#         'articles':queryset,
#     }
#     return render(request, 'article/index.html', context=context)

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'


# def index(request):
#     queryset = Article.objects.all()
#     context = {
#         'articles':queryset,
#     }
#     return render(request, 'article/index.html', context=context)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
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
    print(request.user)
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        instance = form.save(commit=False)
        # instance.user = request.user.user_profile
        # post.user = request.user
        instance.profile = request.user.user_profile
        # instance.profile_id = event_id <int:pk>/3
        #
        instance.save()
        # instance=form.save(commit=False)
        # form.save()
        return redirect('cal:calendar')

    return render(request, 'cal/event.html', {'form': form})


def dash(request):
    # queryset = Event.objects.all()
    # queryset = Event.objects.first()
    # 오늘로 부터 7일전 까지 갖고온다.
    import arrow
    past_datetime = arrow.utcnow().to('Asia/Seoul').replace(hour=0, minute=0, second=0).shift(days=-7).datetime
    events = Event.objects.filter(start_time__gte=past_datetime).order_by('start_time')
    count = 0
    numsum = 0
    for event in events:
        count += 1
        numsum += event.rating
    mean_value = numsum / (count + 1e-7)
    # 갖고온 이벤트들 레이팅값
    # queryset = Event.objects.filter(title__startswith="고은")
    context={
        'events':events,
        'mean_value': mean_value
    }
    return render(request,'cal/index.html',context=context)









# def dash(request):
#
#
#
# def index(request):
#     queryset = Article.objects.all()
#     context = {
#         'articles': queryset,
#     }
#     return render(request, 'article/index.html', context=context)

