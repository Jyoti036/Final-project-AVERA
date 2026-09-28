# AVERA — Django Academic Project

AVERA is an informational and awareness platform around child adoption and child support. It is designed from the uploaded project presentation and class diagram.

## Included modules
- Adoption Information Hub
- Adoption Awareness Hub
- Verified Care Organization Profiles
- Child Information Profiles with privacy note
- Success Story Showcase
- Supporter Feedback System
- FAQ & Help Center
- Wishlist System
- Gift Tracking Journey: Sent → Received → Delivered → Used
- Gift feedback/proof upload
- Milestone & Growth Updates
- Notifications
- Supporter dashboard
- Admin dashboard + Django Admin

## Tech stack
- Python
- Django 5.2+
- SQLite for development
- HTML/CSS/Bootstrap 5
- Bootstrap Icons
- Pillow for image uploads

## Run on Windows / PyCharm
1. Open this folder in PyCharm.
2. Create a virtual environment.
3. Open Terminal:
   `pip install -r requirements.txt`
4. Run:
   `python manage.py makemigrations`
5. Run:
   `python manage.py migrate`
6. Optional demo content:
   `python manage.py seed_data`
7. Start server:
   `python manage.py runserver`
8. Open `http://127.0.0.1:8000/`

## Demo admin
After `seed_data`:
- username: `admin`
- password: `Admin@12345`
- admin URL: `http://127.0.0.1:8000/admin/`

Change the password before any real deployment.

## Important academic-project note
AVERA is implemented as an informational/awareness platform. It does not process legal adoption applications or claim to replace official adoption authorities.

## Main project structure
```
avera_project/
├── manage.py
├── requirements.txt
├── README.md
├── avera/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── main/
    ├── models.py
    ├── forms.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── management/commands/seed_data.py
    ├── templates/main/
    └── static/main/
```
