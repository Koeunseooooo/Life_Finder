from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField

YEARS = [x for x in range(1940, 2021)]


# Create your models here.
class Profile(models.Model):
    interested_tags = (
        # 보일 땐 친구/가족이 보이고 선태가면 앞에 있는게 보이는 구조네. 현재 한 가지만 선택가능
        ('친구/가족과의 시간', '친구/가족과의 시간'),
        ('자기계발', '자기계발'),
        ('운동', '운동'),
        ('취미생활', '취미생활'),
        ('여가생활', '여가생활'),
        ('여행', '여행'),
        ('잠', '잠'),
        ('기타', '기타'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    nickname = models.CharField(max_length=15, verbose_name='닉네임')
    photo = models.ImageField(null=True, blank=True, upload_to="create_profile/%Y/%m/%d", verbose_name='프로필사진')
    # age = models.PositiveIntegerField(blank=True, null=True, verbose_name='나이')
    # birthday = models.DateField(blank=True)
    job = models.CharField(blank=True, max_length=20, verbose_name='직업')
    description = models.TextField(blank=True, max_length=100, verbose_name='소개')
    interested = MultiSelectField(blank=True, max_choices=8, choices=interested_tags,
                                  verbose_name='관심 라이프', default="기타")
    # interested = models.CharField(max_length=15, choices=interested_tags,verbose_name='관심 라이프', default="기타")



    # interested = models.CharField(max_length=15, choices=interested_tags, verbose_name='관심 라이프',default="기타")
    # label = '당신의 관심분야는?', , widget=forms.RadioSelect())
    # interested = models.CharField(max_length=15, choices=Interested_tag, blank=True)
    # interested = models.CharField(max_length=50, default='etc', choices=interested_tags, verbose_name='관심 카테고리')


    def selected_genders_labels(self):
        return [label for value, label in self.fields['genders'].choices if value in self['genders'].value()]



    goal_count = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
