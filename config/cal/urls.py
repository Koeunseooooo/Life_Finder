from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from . import views
app_name = 'cal'
urlpatterns = [
 # path('',views.CalendarView.as_view(),name='calendar'),
 path('', views.CalendarView.as_view(), name='calendar'),
 path('event/new/',views.event, name='event_new'),
 path('event/edit/<int:event_id>',views.event_edit, name='event_edit'),
 # url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
 path('dash/',views.dash,name='dash'),
 path('dash_detail/',views.dash_detail,name='dash_detail'),
 path('no_dash/',views.dash,name='no_dash'),
 # path('event/edit/<int:pk>/delete/', views.delete, name='delete'),

]
