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
    Handles the booking form submission and saves the booking to the database.
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_success')
    else:
        form = BookingForm()

    return render(request, 'bookings/book_table.html', {'form': form})


def booking_success(request):
    """
    Displays a success message after the booking has been submitted.
    """
    return HttpResponse("Thank you! Your booking has been successfully submitted.")