from django.db import models
from django.urls import reverse
from create_profile.models import Profile
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

class Event(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField(default = timezone.now, blank = True)
    # default = timezone.now,
    profile=models.ForeignKey(Profile, related_name='event',on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, default='some_value')

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.rating} </a>'


#
#
#
#
# # Create your models here.
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
#     nickname = models.CharField(max_length=15, verbose_name='닉네임')
#     photo = models.ImageField(blank=True, upload_to="create_profile/%Y/%m/%d", verbose_name='프로필사진')
#     age = models.IntegerField(blank=True, verbose_name='나이')
#     job = models.CharField(blank=True, max_length=20, verbose_name='직업')
#     description = models.TextField(blank=True, max_length=100,verbose_name='소개')
#     goal_count = models.IntegerField(
#         default=0,
#         validators=[
#             MaxValueValidator(100),
#             MinValueValidator(0)
#         ]
#      )