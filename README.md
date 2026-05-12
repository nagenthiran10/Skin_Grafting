# Skin Grafting

## Overview

This repository is a Django-based web application for managing skin grafting workflows. It includes modules for:

- `admins`: administration and approval workflows
- `bioadhesion`: bioadhesion data submission and report handling
- `dermatoplasty`: dermatoplasty data submission and monitoring
- `exfoliation`: exfoliation workflows and reports
- `evaluation`: evaluation and analysis of graft performance
- `monitoring`: monitoring and status tracking across modules

The project uses Django 4.0.x and is configured for MySQL by default.

## Project Structure

- `manage.py` – Django management entrypoint
- `Grafting technique/` – Django project settings and URL configuration
- `admins/`, `bioadhesion/`, `dermatoplasty/`, `exfoliation/`, `evaluation/`, `monitoring/` – application modules
- `template/` – HTML templates used by the Django views
- `static/` – static assets such as CSS, JS, and images
- `media/` – uploaded media and generated reports

## Prerequisites

- Python 3.10+ recommended
- MySQL server for production-style configuration
- `pip` package manager
- Optional: a virtual environment for package isolation

## Setup Instructions

1. Create and activate a Python virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install Django and required packages.

There is a `requirements.txt` file in the repository. Install all dependencies with:

```powershell
pip install -r requirements.txt
```

Or install packages manually:

```powershell
pip install django==4.0.7 mysqlclient reportlab matplotlib pycryptodome
```

3. Configure database settings in `Grafting technique/settings.py`.

The project is configured to use MySQL. Update the database credentials to match your MySQL environment:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'skin grafting',           # Database name
        'USER': 'root',                    # MySQL username
        'PASSWORD': '',                    # MySQL password
        'HOST': 'localhost',               # MySQL host (default: localhost)
        'PORT': 3306,                      # MySQL port (default: 3306)
    }
}
```

Update `NAME`, `USER`, `PASSWORD`, `HOST`, and `PORT` to match your MySQL environment. Ensure the database exists before running migrations.

4. Apply database migrations:

```powershell
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser for admin access:

```powershell
python manage.py createsuperuser
```

6. Run the development server:

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Dashboard

Here is a view of the home page dashboard:

![Home Page](images/Home%20Page.png)

## Notes

- `DEBUG` is enabled in `Grafting technique/settings.py`. Disable this before deploying to production.
- The `SECRET_KEY` in settings should be kept secret and replaced with a secure value.
- Email settings are configured for Gmail SMTP. Replace `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` with your credentials or remove them if not needed.
- Static files are served from `static/` and templates are loaded from `template/`.

## App Descriptions

- `admins`: Handles admin login, approvals, and management dashboards.
- `bioadhesion`: Manages bioadhesion file uploads, scanning, and reports.
- `dermatoplasty`: Handles dermatoplasty file uploads and scanning workflows.
- `exfoliation`: Manages exfoliation submissions and report pages.
- `evaluation`: Manages evaluation files, scan pages, and monitoring results.
- `monitoring`: Tracks workflow status and provides monitoring dashboards.


---

## 🙌 Author

Built by **Nagenthiran** · [GitHub](https://github.com/nagenthiran10)

---

> ⭐ If you found this useful, consider starring the repository!