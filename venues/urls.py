from django.urls import path
from .views import *

urlpatterns = [
    path('',VenuesView.as_view(), name='venues'),

    path('add_venue/',add_venue, name='add_venue'),
    path('add_venue/<int:venue_id>/',add_venue, name='add_venue'),
    path('delete_venue/<int:venue_id>/',delete_venue, name='delete_venue'),
]