from django.contrib import admin
from django.conf.urls import url

from django.urls import path
from . import views
app_name = 'cal'

from django.urls import path, register_converter
from datetime import datetime


urlpatterns = [
 # path('', views.CalendarView.as_view(), name='calendar'),
 url(r'^(?P<date>\d{4}-\d{2}-\d{2})/$', views.CalendarView.as_view(), name='calendar'),
 path('event/new/',views.event, name='event_new'),
 path('event/edit/<int:event_id>',views.event_edit, name='event_edit'),
 path('dash/',views.dash,name='dash'),
 path('dash_detail/',views.dash_detail,name='dash_detail'),
 path('no_dash/',views.dash,name='no_dash'),
]

