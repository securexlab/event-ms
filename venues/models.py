from django.db import models

class Venue(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=300)
    capacity = models.IntegerField()
    parking = models.BooleanField(default=False)
