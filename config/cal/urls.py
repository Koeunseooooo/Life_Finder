from django.contrib import admin
from django.conf.urls import url

from django.urls import path
from . import views
app_name = 'cal'

from django.urls import path, register_converter
from datetime import datetime

# class DateConverter:
#     regex = '\d{4}-\d{2}-\d{2}'
#
#     def to_python(self, value):
#         return datetime.strptime(value, '%Y-%m-%d')
#
#     def to_url(self, value):
#         return value
#
# register_converter(DateConverter, 'yyyy')


urlpatterns = [
 # path('',views.CalendarView.as_view(),name='calendar'),

 path('', views.CalendarView.as_view(), name='calendar'),
 # url(r'^(?P<date>\d{4}-\d{2}-\d{2})/$',views.CalendarView.as_view()),
 path('event/new/',views.event, name='event_new'),
 path('event/edit/<int:event_id>',views.event_edit, name='event_edit'),
 # url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
 path('dash/',views.dash,name='dash'),
 path('dash_detail/',views.dash_detail,name='dash_detail'),
 path('no_dash/',views.dash,name='no_dash'),

 # url(r'^(?P<date>d{4}-d{2}-d{2})/$', views.prev_day),
 # url(r'^/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',views.calendar),

]
# url(r'^(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<date>[0-9]{2})/$', views.CalendarView.as_view()),
# url(r'^(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<date>[0-9]{2})/$', views.CalendarDayView.as_view(), name='day_want'),
# url(r'^(?P<date>\d{4}-\d{2}-\d{2})/$', views.date_url, name='date_url'),
 # path('date/<yyyy:date>/',views.my_date_view, name='my_date_view'),
 # path('event/edit/<int:pk>/delete/', views.delete, name='delete'),

