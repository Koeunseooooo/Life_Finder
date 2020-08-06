from django.contrib import admin
from django.urls import path
from create_profile import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'create_profile'
urlpatterns = [
    path('', views.page, name='page'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
