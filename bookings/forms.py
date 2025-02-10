from django import forms
from .models import Booking, Review


class BookingForm(forms.ModelForm):
    # Override the date and time fields to enforce custom formats
    date = forms.DateField(
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={'placeholder': 'dd-mm-yyyy', 'type': 'text'}  # using 'text' so the placeholder shows
        ),
        input_formats=['%d-%m-%Y'],
    )
    time = forms.TimeField(
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={'placeholder': 'HH:MM', 'type': 'text'}  # using 'text' for the placeholder
        ),
        input_formats=['%H:%M'],
    )

    # Define the form fields and provide help text for the date and time fields
    # class Meta is a nested class inside the BookingForm class that provides metadata about the form
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests']
        help_texts = {
            'date': 'Enter the booking date in dd-mm-yyyy format (e.g. 05-08-2025).',
            'time': 'Enter the booking time in HH:MM format (e.g. 18:00).',
        }

class ReviewForm(forms.ModelForm):
    """
    A form for users to submit reviews.
    """
    class Meta:
        model = Review
        fields = ['name', 'email', 'comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }        
