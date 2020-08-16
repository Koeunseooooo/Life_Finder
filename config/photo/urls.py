from django.urls import path
from .views import PhotoList, PhotoDelete, PhotoDetail, PhotoUpdate, PhotoCreate, PhotoLike, PhotoLikeList, PhotoMyList

app_name = "photo"
urlpatterns = [
    path("mylist/", PhotoMyList.as_view(), name='mylist'),
    path("create/", PhotoCreate.as_view(), name='create'),
    path("like/<int:photo_id>/", PhotoLike.as_view(), name='like'),
    path("delete/<int:pk>/", PhotoDelete.as_view(), name='delete'),
    path("update/<int:pk>/", PhotoUpdate.as_view(), name='update'),
    path("detail/<int:pk>/", PhotoDetail.as_view(), name='detail'),
    path("like/", PhotoLikeList.as_view(), name="like_list"),
    path("", PhotoList.as_view(), name='index'),
]

from django.conf.urls.static import static

from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)