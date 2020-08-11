from django.contrib import admin
from cal.models import Event
from .forms import EventForm


# admin.site.register(Event)

@admin.register(Event)
class CountAdmin(admin.ModelAdmin):
    form = EventForm
    pass
