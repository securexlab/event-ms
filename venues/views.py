from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Venue
from .forms import VenueForm

# Create your views here.
class VenuesView(LoginRequiredMixin, TemplateView):
    

    def get_context_data(self, **kwargs):
        venues = Venue.objects.all()
        venues_count = Venue.objects.count()
        context = {'venues': venues, 'venues_count': venues_count}
        return context

    template_name = 'venues.html'

def add_venue(request,venue_id=None):

    if venue_id:
        venue = get_object_or_404(Venue,id=venue_id)
        form = VenueForm(instance=venue)
    else:
        venue = None
        form = VenueForm()

    if request.method == 'POST':
        # Capture the form data
        name = request.POST.get('name')
        address = request.POST.get('address')
        capacity = request.POST.get('capacity')
        parking = request.POST.get('parking') == 'on'

        if venue:
            venue.name = name
            venue.address = address
            venue.capacity = capacity
            venue.parking = parking
        else:
            venue = Venue(name=name, address=address, capacity=capacity, parking=parking)
            print("Venue created")

        # Create a new venue and save it
        venue.save()

        # Redirect after successful form submission
        return redirect('venues')  # Replace with the name of the view to display the list of venues

    # If GET request, render the form template
    return render(request, 'form/venue_form.html', {'form': form})

def delete_venue(request,venue_id):
    venue = get_object_or_404(Venue,id=venue_id)
    venue.delete()
    return redirect('venues')  # Replace with the name of the view to display the list of venues