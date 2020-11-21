from django.http import Http404
from django.shortcuts import render
from .models import Flight, Passenger

# Create your views here.
def index(request):
    context = {
        'flights': Flight.objects.all()
    }
    return render(request, "flights/index.html", context)

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Exception as e:
        raise Http404("Flight does not exist.")

    context = {
        'flight': flight,
        'passengers': flight.passengers.all(),
        'non_passengers': Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    if request.method == "POST":
        try:
            passenger_id = int(request.POST["passenger"])
            passenger = Passenger.objects.get(pk=passenger_id)
            flight = Flight.objects.get(pk=flight_id)
            passenger.flights.add(flight)
        except Exception as e:
            raise Http404("Error with booking.")

        context = {
            'passenger': passenger,
            'flight': flight
        }

        return render(request, 'flights/booked.html', context)
