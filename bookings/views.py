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

from django.contrib.admin.views.decorators import staff_member_required
from datetime import date, datetime, timedelta
from .models import Booking  # Ensure Booking is imported
from collections import defaultdict, OrderedDict
from .forms import ReviewForm
from .models import Review

def home(request):
    approved_reviews = Review.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'bookings/home.html', {
        'approved_reviews': approved_reviews,
        # any other context variables
    })

def check_capacity(new_booking):
    """
    For a given new_booking instance (unsaved), this function calculates
    the total number of guests already reserved for bookings whose 2-hour window
    overlaps with the new_booking's 2-hour window.
    """
    booking_date = new_booking.date
    new_start = datetime.combine(booking_date, new_booking.time)
    new_end = new_start + timedelta(hours=2)

    # Get all bookings for that date
    existing_bookings = Booking.objects.filter(date=booking_date)
    total_reserved = 0

    for booking in existing_bookings:
        existing_start = datetime.combine(booking.date, booking.time)
        existing_end = existing_start + timedelta(hours=2)
        # Check if the new booking overlaps with the existing booking's 2-hour window:
        if new_start < existing_end and existing_start < new_end:
            total_reserved += booking.guests

    return total_reserved


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
    If valid, checks capacity for a 2-hour window (80% of 50 seats, i.e. 40 seats).
    If the new booking would exceed capacity, returns an error.
    Otherwise, saves the booking, sends a confirmation email, and redirects.
    """
    initial_data = {}
    if 'time' in request.GET:
        initial_data['time'] = request.GET.get('time')
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Get an unsaved booking instance
            new_booking = form.save(commit=False)
            
            # Check capacity for the new booking's 2-hour window
            total_reserved = check_capacity(new_booking)
            allowed_capacity = 40  # 80% of 50 seats
            
            if total_reserved + new_booking.guests > allowed_capacity:
                form.add_error(
                    None,
                    "Cannot accept booking: The requested time slot is nearly full. Please reduce the number of guests or try a different time."
                )
                return render(request, 'bookings/book_table.html', {'form': form})
            
            # Save the booking since capacity is sufficient
            new_booking.save()
            messages.success(request, f'Booking for {new_booking.date} at {new_booking.time} confirmed!')
            
            # Send a confirmation email to the customer
            send_mail(
                subject="Your Booking Confirmation",
                message=(
                    f"Dear {new_booking.name},\n\n"
                    f"Your booking for {new_booking.date} at {new_booking.time} is confirmed.\n"
                    "We look forward to welcoming you at Coughlan's!\n\n"
                    "Thank you."
                ),
                from_email="noreply@coughlans.com",
                recipient_list=[new_booking.email],
                fail_silently=False,
            )
            
            return redirect('booking_success', booking_id=new_booking.id)
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

@staff_member_required
def weekly_calendar(request):
    """
    Displays a weekly calendar view of bookings.
    Only accessible by staff. Allows navigation to previous and next weeks.
    The view checks for a GET parameter 'week_start' to determine the week to display (formatted as 'YYYY-MM-DD').
    If provided, it parses that value to determine the starting Monday, if not, it defaults to the current week's Monday.
    It then iterates over 7 days (Monday to Sunday), querying for bookings on each day and storing them in an ordered dictionary.
    It also computes the previous and next week start dates (as strings) to help build navigation links in the template.
    The view is decorated with @staff_member_required so only staff can access it.
    """
    # Determine the week start from GET parameter if provided, otherwise use current week.
    week_start_str = request.GET.get("week_start")
    if week_start_str:
        try:
            week_start = datetime.strptime(week_start_str, "%Y-%m-%d").date()
        except ValueError:
            week_start = date.today() - timedelta(days=date.today().weekday())
    else:
        week_start = date.today() - timedelta(days=date.today().weekday())

    # Create an ordered dictionary of bookings per day (Monday to Sunday)
    bookings_by_day = OrderedDict()
    for i in range(7):
        current_day = week_start + timedelta(days=i)
        daily_bookings = Booking.objects.filter(date=current_day).order_by('time')
        bookings_by_day[current_day] = daily_bookings

    # Calculate previous and next week start dates for navigation
    previous_week = week_start - timedelta(days=7)
    next_week = week_start + timedelta(days=7)

    context = {
        'week_start': week_start,
        'bookings_by_day': bookings_by_day,
        'previous_week': previous_week.strftime("%Y-%m-%d"),
        'next_week': next_week.strftime("%Y-%m-%d"),
    }
    return render(request, 'bookings/weekly_calendar.html', context)


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

def cancel_lookup(request):
    """
    Displays a form for users to look up their bookings by email.
    If bookings are found, they are listed with options to cancel.
    """
    bookings_found = None
    if request.method == 'POST':
        email = request.POST.get('email')
        # Optionally, you could add more criteria (like a booking reference)
        if email:
            bookings_found = Booking.objects.filter(email__iexact=email)
            if not bookings_found:
                messages.error(request, "No bookings found for that email address.")
        else:
            messages.error(request, "Please enter an email address.")
    
    return render(request, 'bookings/cancel_lookup.html', {
        'bookings_found': bookings_found
    })

def confirm_cancel(request, booking_id):
    """
    Displays a confirmation page asking if the user really wants to cancel their booking.
    If confirmed, the booking is deleted and a thank you message is displayed.
    The view fetches the booking using booking_id.
    On a POST request (i.e., when the user clicks the final cancel button), the booking is deleted and a success message is displayed.
    The user is then redirected to the homepage.
    On a GET request, the view renders the confirmation page.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        # Delete the booking and set a success message
        booking.delete()
        messages.success(request, "Thanks, we hope to see you soon at Coughlan's!")
        # Optionally, redirect to the homepage or a dedicated cancellation success page
        return redirect('home')
    
    # Render the confirmation page (GET request)
    return render(request, 'bookings/cancel_confirm.html', {'booking': booking})

def update_booking(request, booking_id):
    """
    Allows a customer to modify/reschedule their booking after confirming their email.
    The form is pre-populated with the existing booking data.
    Retrieves the booking by ID.
    On a POST request, it compares the submitted email with the booking's email.
    If the email verification passes and the form is valid, it saves the updated booking and redirects to the booking success page.
    On a GET request, it pre-populates the form with the current booking data.
    """
    booking = get_object_or_404(Booking, id=booking_id)
    
    # On POST, verify email and update booking
    if request.method == 'POST':
        # Assume the update form has an extra field 'confirm_email' for verification
        confirm_email = request.POST.get('confirm_email')
        if not confirm_email or confirm_email.lower() != booking.email.lower():
            messages.error(request, "The email provided does not match our records.")
        else:
            form = BookingForm(request.POST, instance=booking)
            if form.is_valid():
                updated_booking = form.save()
                messages.success(request, "Your booking has been updated successfully!")
                # Optionally, send an email confirmation for the update here
                return redirect('booking_success', booking_id=updated_booking.id)
            else:
                messages.error(request, "Please correct the errors below.")
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'bookings/update_booking.html', {
        'form': form,
        'booking': booking
    })

def update_booking_lookup(request):
    """
    Displays a form for users to look up their booking(s) by email.
    If bookings are found, they are listed with links to update each booking.
    """
    bookings_found = None
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            bookings_found = Booking.objects.filter(email__iexact=email)
            if not bookings_found:
                messages.error(request, "No bookings found for that email address.")
        else:
            messages.error(request, "Please enter your email address.")
    
    return render(request, 'bookings/update_booking_lookup.html', {
        'bookings_found': bookings_found
    })

def submit_review(request):
    """
    Allows users to submit a review.
    Reviews will be pending approval until an admin approves them.
    """
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your review! It will appear on our site once approved.")
            return redirect('home')  # or any appropriate page
    else:
        form = ReviewForm()
    return render(request, 'bookings/submit_review.html', {'form': form})

def review_ticker(request):
    """
    Retrieves approved reviews to be displayed on a ticker.
    """
    reviews = Review.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'bookings/review_ticker.html', {'reviews': reviews})


