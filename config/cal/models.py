from django.db import models
from django.urls import reverse
from create_profile.models import Profile
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
# from PIL import Image
#
# im=Image.open('hello.jpg')
# print(im.size)

class Event(models.Model):
    cateegory_tags = (
        # 보일 땐 친구/가족이 보이고 선태가면 앞에 있는게 보이는 구조네. 현재 한 가지만 선택가능
        ('친구/가족과의 시간', '친구/가족과의 시간'),
        ('자기계발', '자기계발'),
        ('운동', '운동'),
        ('취미생활', '취미생활'),
        ('여가생활', '여가생활'),
        ('여행', '여행'),
        ('일', '일'),
        ('기타', '기타'),
    )
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    profile=models.ForeignKey(Profile, related_name='event',on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, default='enter your value')
    category = models.CharField(choices=cateegory_tags,max_length=15,blank=True,default="기타")
    def __str__(self):
        return '{}/ {}/ {}'.format(self.id, self.title, self.start_time, self.rating)

    #적용이 안되는 property,,,,
    # @property
    # def created_at_korean_time(self):
    #     korean_timezone = timezone(settings.TIME_ZONE)
    #     return self.created_at_korean_time(korean_timezone)

    # @property
    # def get_html_url(self):
    #     url = reverse('cal:event_edit', args=(self.id,))
    #     # f'<a href="{url}"> {self.rating} </a>'
    #
    #     result = []
    #     for a in {self.rating}:
    #         while a>0:
    #             result.append('|||||||||')
    #             a-=1
    #
    #     final_result=' '.join(result)
    #
    #     return f'<a href="{url}">{final_result}</a>'

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        # f'<a href="{url}"> {self.rating} </a>'

        result = ''
        for a in {self.title}:
            result += a[:7]

        return f'<a href="{url}">{result}</a>'


