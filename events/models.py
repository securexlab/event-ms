from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200)
    #type should be selected from the dropdown
    type = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    venue = models.ForeignKey('venues.Venue', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_images', blank=True)
    description = models.TextField()

