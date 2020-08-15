from django.contrib import admin
from django.urls import path
from create_profile import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'create_profile'
urlpatterns = [
    # path('', views.page, name='page'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:pk>/', views.profile_look, name='profile_look'),
    path('profile/<int:pk>/edit/', views.profile_edit, name='profile_edit'),
    path('profile/register/', views.register, name='register'),
    path('goal/', views.goal_get, name='goal_get'),

    path('login_success/',views.login_success,name='login_success'),
    path('login_please/', views.need_login, name='need_login'),
]

urlpatterns += staticfiles_urlpatterns()
