# This file contains the view functions for the bookings app.
# import the necessary modules
from django.shortcuts import render, redirect # render is used to render the HTML template
from .forms import BookingForm # import the BookingForm class from the forms.py file
from django.http import HttpResponse # import the HttpResponse class to return a simple response
from django.contrib import messages # import the messages module to display messages to the user
from .models import Booking # import the Booking model
from django.contrib.admin.views.decorators import staff_member_required # import the staff_member_required decorator
from django.core.mail import send_mail # import the send_mail function to send emails
from django.shortcuts import render, redirect, get_object_or_404 # import the get_object_or_404 function to get an object by ID or return a 404 error



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

def cancel_booking(request, booking_id):
    """
    Allows a customer to cancel a booking if they provide the correct email.
    It fetches the booking by ID.
    On a POST request it compares the submitted email with the booking's email.
    If the emails match, the booking is deleted and a success message is displayed, otherwise an error message is shown.
    On a GET request, it renders the cancellation confirmation page.
    """
    # Retrieve the booking or return a 404 if not found.
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        # Retrieve the email entered by the user in the cancellation form.
        email_input = request.POST.get('email')
        
        # Check if the provided email matches the booking's email (case-insensitive)
        if email_input and email_input.lower() == booking.email.lower():
            # Delete the booking from the database.
            booking.delete()
            messages.success(request, "Your booking has been cancelled.")
            return redirect('home')
        else:
            messages.error(request, "Email address does not match our records. Cancellation failed.")
    
    # Render the cancellation confirmation page.
    return render(request, 'bookings/cancel_booking.html', {'booking': booking})

def update_booking(request, booking_id):
    """
    Allows a customer to update their booking details after confirming their email.
    It fetches the booking by ID.
    On a POST request it compares the submitted email with the booking's email.
    If the emails match, the booking is updated and a success message is displayed, otherwise an error message is shown.
    On a GET request, it renders the update booking form with the existing booking data.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        # Retrieve the confirmation email from the form.
        confirm_email = request.POST.get('confirm_email')
        if confirm_email and confirm_email.lower() == booking.email.lower():
            # Create a form instance with the POST data and the existing booking.
            form = BookingForm(request.POST, instance=booking)
            if form.is_valid():
                updated_booking = form.save()
                messages.success(request, "Your booking has been updated!")
                return redirect('booking_success', booking_id=updated_booking.id)
        else:
            messages.error(request, "Email address does not match our records. Update failed.")
            # Create a form instance with the POST data to preserve entered data.
            form = BookingForm(request.POST, instance=booking)
    else:
        # For GET requests, prepopulate the form with the existing booking data.
        form = BookingForm(instance=booking)
    
    return render(request, 'bookings/update_booking.html', {'form': form, 'booking': booking})


