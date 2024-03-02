from django.shortcuts import render
from .models import Location

# Create your views here.
def locations(request):
    current_location = request.session.get('current_location')


    locations_list = Location.objects.all()
    context={
        'locations' : locations_list,
        'current_location': current_location,
    }
    return render(request, 'locations/locations.html', context)