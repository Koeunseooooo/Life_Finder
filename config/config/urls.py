
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calendar/',include('cal.urls')),
    path('',include('main.urls')),
    path('create/',include('create_profile.urls')),
    path('dash/',include('dashboard.urls')),

    path('accounts/',include('allauth.urls')),
    path('photo/', include('photo.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)