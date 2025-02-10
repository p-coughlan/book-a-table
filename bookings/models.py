from django.db import models

# Create your models here.

class Booking(models.Model):
    """
    A model to store booking information
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"
    

class Review(models.Model):
    """
    A model to store reviews
    """
    name = models.CharField(max_length=200)
    email = models.EmailField()
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # Optional: a rating out of 5
    approved = models.BooleanField(default=False)    # Only approved reviews are displayed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.name} ({'Approved' if self.approved else 'Pending'})"

