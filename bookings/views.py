# This file contains the view functions for the bookings app.
# import the necessary modules
from django.shortcuts import render, redirect # render is used to render the HTML template
from .forms import BookingForm # import the BookingForm class from the forms.py file
from django.http import HttpResponse # import the HttpResponse class to return a simple response


def home(request):
    """
    Renders the homepage with a link to the booking form.
    """
    return render(request, 'bookings/home.html')


def book_table(request):
    """
    Displays the booking form and processes the form submission.
    """
    initial_data = {}
    # Check if the 'date' parameter is in the URL query parameters
    if 'time' in request.GET:
        initial_data['time'] = request.GET.get('time') # set the 'time' field in the form to the value in the URL
    
    # Check if the form has been submitted
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_success') # redirect to the booking success page
    else:
        form = BookingForm(initial=initial_data) # create a new form with the initial data
    
    return render(request, 'bookings/book_table.html', {'form': form}) # render the booking form template with the form



def booking_success(request):
    """
    Displays a success message after the booking has been submitted.
    """
    return HttpResponse("Thank you! Your booking has been successfully submitted.")

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
