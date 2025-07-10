# EVENTNEST
Django based simplified Event Management System where users can create events, register attendees, and view attendee lists per event.


# Problem Statement

To build a backend for a simplified Event Management System. Users should be able to create events, register attendees, and view attendee lists per event. Achieve the below-mentioned features.

1. Create a new event with fields: name, location, start_time, end_time, max_capacity.
2. List all upcoming events.
3. Register an attendee (name, email) for a specific event. Make sure to prevent overbooking and  duplicate registrations with email.
4. List all registered attendees for an event.


# Features

- Create Events with Maximum Capacity
- Register Attendees for an event
- List all attendees for a given event
- API support via DRF


# Tech Stack

- Django, Django REST Framework, PostgreSQL, PostGIS



<!-- GETTING STARTED -->
# Getting Started

## 1. Install System Packages

You’ll need:

* PostgreSQL

* PostGIS extension

* Python 3.10+

* virtualenv or venv

### Ubuntu / Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib postgis libpq-dev
```

### Mac OS:
```
brew install postgresql
brew install postgis
brew services start postgresql
```

## 2. Create Database & PostGIS Extension
```
# Login to Postgres

sudo -u postgres psql

# In psql shell:

CREATE DATABASE <DB_NAME>;

CREATE USER <DB_USER> WITH PASSWORD '<DB_PASSWORD>';

GRANT ALL PRIVILEGES ON DATABASE <DB_NAME> TO <DB_USER>;

ALTER DATABASE <DB_NAME> OWNER TO <DB_USER>;

ALTER USER <DB_USER> SUPERUSER;  # This is needed for the tests to create postgis extension for the test db

\c <DB_NAME>

CREATE EXTENSION postgis;
\q
```



## 3. Project Setup
### 1. Clone Repository

```
git clone https://github.com/akshaybabu09/eventnest.git
cd eventnest
```

### 2. Set Up Python Environment

```
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Add Environment Variables

.env
```
SECRET_KEY=<SECRET_KEY>
DB_NAME=<DATABASE_NAME>
DB_USER=<DATABASE_USER>
DB_PASSWORD=<DATABASE_PASSWORD>
DB_HOST=<DATABASE_HOST>
```

### 4. Run Migrations and create superuser

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run Server

```
python manage.py runserver
```
Go to http://127.0.0.1:8000/admin/

### 6. Run Tests

```
python manage.py test


Found 9 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.........
----------------------------------------------------------------------
Ran 9 tests in 0.060s

OK
Destroying test database for alias 'default'...

```

### 7. Swagger Documentation

Go to http://127.0.0.1:8000/api/docs/redoc/ or http://localhost:8000/api/docs/ 


### 8. Database Schema

```
Have included the migration files for reference
```



## 4. Troubleshooting
If you need to install GEOS, GDAL, etc

On Ubuntu
```
sudo apt install binutils libproj-dev gdal-bin libgdal-dev libgeos-dev
```

Mac OS
```
brew install gdal proj geos
```

