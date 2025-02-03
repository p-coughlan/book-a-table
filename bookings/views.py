# This file contains the view functions for the bookings app.
# import the necessary modules
from django.shortcuts import render, redirect # render is used to render the HTML template
from .forms import BookingForm # import the BookingForm class from the forms.py file
from django.http import HttpResponse # import the HttpResponse class to return a simple response
from django.contrib import messages # import the messages module to display messages to the user
from .models import Booking # import the Booking model
from django.contrib.admin.views.decorators import staff_member_required # import the staff_member_required decorator
from django.core.mail import send_mail # import the send_mail function to send emails


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
    If the form is valid, the booking is saved to the database and a success message is displayed.
    Sends a confirmation email to the customer.
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

            # Send an email to the customer
            send_mail(
                subject="Your Booking Confirmation",
                message=(
                    f"Dear {booking.name},\n\n"
                    f"Your booking for {booking.date} at {booking.time} is confirmed.\n"
                    "We look forward to welcoming you at COUGHLAN'S!\n\n"
                    "Thank you."
                ),
                from_email="noreply@coughlans.com",
                recipient_list=[booking.email], # list containing the recipient's email address
                fail_silently=False,
            )
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

@staff_member_required # Only staff users can access this view
def booking_list(request):
    """
    Displays a list of all bookings. Accessible only to staff users.
    """
    bookings = Booking.objects.all().order_by('-id')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


