from django.shortcuts import render, redirect
from .forms import BookingForm

# Create your views here.
def book_table(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_success')
    else:
        form = BookingForm()

    return render(request, 'bookings/book_table.html', {'form': form})