from django.forms import ModelForm, DateInput, HiddenInput,TextInput
from cal.models import Event
from .widgets import RateitjsWidget
from django.utils import timezone


class EventForm(ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'title': TextInput(attrs={'placeholder': '  ex)  야호!  오늘 코딩 오류 한번에 잡았다! '}),
            'rating': RateitjsWidget,
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ['title', 'start_time','category', 'rating']
        # , 'profile'


    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats =  ('%Y-%m-%dT%H:%M',)



