from django.contrib import admin

# Register your models here.
from .models import Booking
from .models import Review

admin.site.register(Booking)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin class for managing Review instances in the Django admin interface.

    This class customizes the display, filtering, and search options for Review objects.
    It also provides an action to approve selected reviews.
    """
    list_display = ('name', 'email', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('name', 'email', 'comment')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        """
        Custom admin action to approve selected reviews.

        Args:
            request: The current HttpRequest object.
            queryset: The QuerySet of Review objects selected by the admin user.
        """
        queryset.update(approved=True)
    approve_reviews.short_description = "Approve selected reviews"
