from datetime import datetime, timedelta
from calendar import HTMLCalendar


from django.contrib.auth.models import User
from .models import Event
from create_profile.models import Profile


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

# class Calendar(HTMLCalendar):
#     def __init__(self, year=None, month=None,day=None):
#         self.year = year
#         self.month = month
#         self.day = day
#         super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for event in events_per_day:
            d += f"<li> {event.get_html_url} </li>"

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
            # filter_date = Event.objects.all().filter(start_time__day=day)
            # return f"<td><span class='date'><a href=''>{day}</a></span><ul>{d}</ul></td>", filter_date

        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    # issue. 달력 문제 해결 , user 값 넣고 filter 주기
    def formatmonth(self, user, withyear=True):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month).filter(profile= user.user_profile)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal