# This file contains the view functions for the bookings app.
# import the necessary modules
from django.shortcuts import render, redirect
from .forms import BookingForm
from django.http import HttpResponse

# Create your views here.
# This view function will handle the form submission and save the booking to the database.
def book_table(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_success')
    else:
        form = BookingForm()

    return render(request, 'bookings/book_table.html', {'form': form})

# This view function will display a success message after the booking has been submitted.
def booking_success(request):
    return HttpResponse("Thank you! Your booking has been successfully submitted.")