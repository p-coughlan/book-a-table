"""
URL configuration for restaurant_booking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# import the view functions from the bookings app
from bookings.views import home, book_table, booking_success, available_timeslots

# define the URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('book/', book_table, name='book_table'),
    path('success/', booking_success, name='booking_success'),
    path('timeslots/', available_timeslots, name='available_timeslots'),
]
