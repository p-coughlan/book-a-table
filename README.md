# book-a-table
A CRUD restaurant table booking application using Python, Django and SQL

Project Setup Instructions
1. Set Up a Virtual Environment
python3 -m venv venv
source venv/bin/activate  # (For Mac/Linux)

2. Install Dependencies
pip install --upgrade pip  
pip install django djangorestframework  
pip freeze > requirements.txt  

3. Initialize Django Project
django-admin startproject restaurant_booking .

4. Configure SQLite Database
Open restaurant_booking/settings.py
Ensure DATABASES is set to:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

5. Apply Migrations
python manage.py migrate

6. Run Development Server
python manage.py runserver
Open http://127.0.0.1:8000/ to confirm it's working.

7. Create the bookings App
Generated the Django app using:
python manage.py startapp bookings
Added the app to INSTALLED_APPS in restaurant_booking/settings.py.

8. Defined the Booking Model
Added a Booking model in bookings/models.py to store reservation details (name, email, date, time, etc.).

9. Database Migrations
Generated and applied database migrations for the new model using:
python manage.py makemigrations
python manage.py migrate

10. Admin Panel Setup
Registered the Booking model in Django Admin by editing bookings/admin.py.
Created a superuser to access the admin interface:
python manage.py createsuperuser
Access the admin panel at http://127.0.0.1:8000/admin/ using the superuser credentials.

11. Created the bookings App:
Generated a new Django app and added it to INSTALLED_APPS.

12. Defined the Booking Model:
Added a model in bookings/models.py to store reservation details.

13. Registered the Booking Model in Admin:
Updated bookings/admin.py and created a superuser to manage bookings via Django’s admin interface.

13. Created a Booking Form:
 - Added bookings/forms.py with a BookingForm that includes fields for name, email, phone, date, time, and guests.
 - Customized the date and time fields with specific input formats (dd-mm-yyyy and HH:MM), placeholders, and help text.

14. Built the Booking View:
Added a view in bookings/views.py to handle displaying the form and saving the booking.

13. Created a Template:
Set up bookings/templates/bookings/book_table.html to render the booking form.

14. Configured URLs:
Updated restaurant_booking/urls.py with paths for the booking form (/book/) and a simple success page (/success/).

15. Implemented a Success Page:
Created a basic view that confirms a successful booking after form submission.

---------------------------------------------------
Superuser for Admin Access
Username: admin
Email address: admin@booking.com
Password: reservations

---------------------------------------------------
Current progress:
Display messages in the Base Template

---------------------------------------------------

ISSUES AND IMPROVEMENTS:

Booking form was difficult to use with no guidance on date and time format
I used placeholders and help text to guide user with the intention of creating a more user friendly UI further down the line

Booking confirming when under or at capacity but unresponsive when over:
Non-field error missing from template ,added:
{% if form.non_field_errors %}
  <div class="alert alert-danger">
    {{ form.non_field_errors }}
  </div>
{% endif %}

Admin Login:
At present, staff are sent to directly to the Django Admin Panel.
A custom view would be better.
Create custom view and link to that instead. 

Update booking: 
This could be problematic for the restaurant at late notice?
Implement a 24 hr rule in the booking & update functions.


---------------------------------------------------

Specfics of Coughlan's table management. I need to keep this as simple as possible. 
Seating capacity: 50
Open for lunch: 11am to 3pm
Open for dinner: 5pm to 9pm
The restaurant bar is open 11am to 11pm but the seating times will be in 2 sittings: 
What is the most effective way to manage these tables at an 80% capacity to allow for walk-in diners?

Define Total Capacity and Allowed Reservation Capacity:

The restaurant has a total capacity of 50 seats.
For reservations, only 80% (i.e. 40 seats) is available.
Each booking occupies a 2‑hour window (e.g., a booking at 12:00 occupies 12:00–14:00).
When a new booking is made, you need to check for overlapping bookings (on the same date) whose 2‑hour windows overlap the new booking’s window.
If the sum of guests from overlapping bookings plus the new booking’s guests exceeds 40, you reject the booking.

* Create a Helper Function to Check Capacity 
* Update book_table View to Use the New Capacity Check

---------------------------------------------------