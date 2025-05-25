# Rent API 🏠

A RESTful API for managing a rental property platform, built with Django and Django REST Framework. This API supports user authentication, property listings, lease agreements, maintenance requests, and more.

---

## 🚀 Features

- User registration and authentication (JWT-based)
- Property listing and management
- Lease creation and tracking
- Maintenance request system
- Notifications for key events
- Role-based access control (e.g. Tenant, Landlord)
- Media uploads (property images, attachments)

---

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT via `djangorestframework-simplejwt`
- **Database**: SQLite (Dev), PostgreSQL (Prod recommended)
- **Media Storage**: Local filesystem or cloud (e.g. AWS S3)
- **Deployment**: (Insert your deployment platform e.g. Render, Heroku, Docker)

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/oys2021/RentApi.git
cd RentApi

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create a superuser (admin)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
