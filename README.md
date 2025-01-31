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