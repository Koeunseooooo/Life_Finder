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
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    profile=models.ForeignKey(Profile, related_name='event',on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, default='enter your value')

    def __str__(self):
        return '{}/ {}/ {}'.format(self.id, self.title, self.start_time, self.rating)

    #적용이 안되는 property,,,,
    # @property
    # def created_at_korean_time(self):
    #     korean_timezone = timezone(settings.TIME_ZONE)
    #     return self.created_at_korean_time(korean_timezone)

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        # f'<a href="{url}"> {self.rating} </a>'

        result = []
        for a in {self.rating}:
            while a>0:
                result.append('●')
                a-=1

        final_result=' '.join(result)

        return f'<a href="{url}">{final_result}</a>'

