from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests']
        
    # add the date and time widgets to the form with the correct input types and placeholders
    widgets = {
    'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
    'time': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'HH:MM'}),
}

