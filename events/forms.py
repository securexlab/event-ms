from .models import Event
from django import forms

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'short_name', 'type', 'start', 'end', 'venue', 'image', 'description']
