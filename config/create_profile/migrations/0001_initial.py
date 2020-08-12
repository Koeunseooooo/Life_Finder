# Generated by Django 2.2.9 on 2020-08-12 09:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=15, verbose_name='닉네임')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='create_profile/%Y/%m/%d', verbose_name='프로필사진')),
                ('job', models.CharField(blank=True, max_length=20, verbose_name='직업')),
                ('description', models.TextField(blank=True, max_length=100, verbose_name='소개')),
                ('interested', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('친구/가족과의 시간', '친구/가족과의 시간'), ('자기계발', '자기계발'), ('운동', '운동'), ('취미생활', '취미생활'), ('여가생활', '여가생활'), ('여행', '여행'), ('잠', '잠'), ('기타', '기타')], default='기타', max_length=36, verbose_name='관심 라이프')),
                ('goal_count', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
