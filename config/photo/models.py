from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from create_profile.models import Profile

# Create your models here.

class Photo(models.Model):
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_profile')
    title = models.CharField(max_length=20)
    text = models.TextField()
    image = models.ImageField(upload_to= 'timeline_photo/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, related_name='like_post', blank=True)
    favorite = models.ManyToManyField(User, related_name='favorite_post', blank=True)


    def __str__(self):
        return "text : "+self.text

    class Meta:
        ordering = ['-created']


    def get_absolute_url(self):
        return reverse('photo:index', args=[self.id])


# class Comment(models.Model):
#     name = models.CharField(max_length=30, blank=True)
#     address = models.CharField(max_length=100, blank=True)
#     age = models.IntegerField(blank=True, null=True)


class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='photo_comment')
    comment_author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment_author_profile')
    text = models.TextField()

    def __str__(self):
        return self.text