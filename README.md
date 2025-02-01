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

---------------------------------------------------
Superuser for Admin Access
Username: admin
Email address: admin@booking.com
Password: reservations

---------------------------------------------------
Current progress:
Create success page