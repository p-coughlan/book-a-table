# This file contains the view functions for the bookings app.
# import the necessary modules
from django.shortcuts import render, redirect # render is used to render the HTML template
from .forms import BookingForm # import the BookingForm class from the forms.py file
from django.http import HttpResponse # import the HttpResponse class to return a simple response
from django.contrib import messages # import the messages module to display messages to the user
from .models import Booking # import the Booking model

def home(request):
    """
    Renders the homepage with a link to the booking form.
    """
    return render(request, 'bookings/home.html')

# After saving the booking, we call messages.success(...) to create a success message.
# This message will be available in the next view rendered after the redirect.
def book_table(request):
    """
    Displays the booking form and processes the form submission.
    """
    initial_data = {}
    if 'time' in request.GET:
        initial_data['time'] = request.GET.get('time')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            # Add a success message using the booking details
            messages.success(request, f'Booking for {booking.date} at {booking.time} confirmed!')
            # Redirect to success page with the booking's ID included in the URL
            return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm(initial=initial_data)
    
    return render(request, 'bookings/book_table.html', {'form': form})


def booking_success(request, booking_id):
    """
    Displays the booking success page with booking details.
    """
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'bookings/booking_success.html', {'booking': booking})

def available_timeslots(request):
    """
    Displays a simple visual representation of available timeslots.
    For demonstration, timeslots are hardcoded.
    """
    # Hardcoded list of timeslots for demonstration purposes.
    timeslots = [
        {'time': '18:00', 'available': True},
        {'time': '18:30', 'available': False},
        {'time': '19:00', 'available': True},
        {'time': '19:30', 'available': True},
        {'time': '20:00', 'available': False},
    ]
    return render(request, 'bookings/timeslots.html', {'timeslots': timeslots})

def booking_list(request):
    """
    Displays a list of all bookings.
    """
    # Retrieve all bookings, ordered by newest first
    bookings = Booking.objects.all().order_by('-id') # -id orders by descending ID
    return render(request, 'bookings/booking_list.html', {'bookings': bookings}) # Pass the bookings to the template

