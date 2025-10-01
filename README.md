
# Task Management Application with Task Completion Report

This project is a **Task Management Application** built with **Django** that includes task assignment, completion reporting, and role-based access. It provides both API endpoints and an admin panel for managing tasks and tracking user activity.

## 🚀 Features
- User Registration and login Functionality
- Secure authentication with JWT-based authentication
- Admin panel
- Role based access
- Create new tasks with asign to user
- Retrieve tasks assigned to a specific user
- Task Completion Report and Worked Hours

---

## 📂 Project Structure

```
TaskManagement-Noviindus/
├── users/                  # Authentication 
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            # Custom User model with roles
│   ├── serializers.py       # Serializers for User & Auth
│   ├── urls.py              # App-specific routes
│   ├── views.py             # API Views
│
├── config/                  # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Django settings 
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py
│
├── common/                  # Authentication 
│   ├── __init__.py
│   ├── admin.py
│   ├── cookie_auth.py       # Custom Cookie setup
│   ├── models.py            
│   ├── urls.py              
│   ├── views.py
├── tasks/                  # Task CRUD fuctionality 
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            
│   ├── serializers.py       # Serializers for User & Auth
│   ├── urls.py              # App-specific routes
│   ├── views.py             # API Views
├── template/                #UI part 
│   ├── include/             # Navbar, footbar, Error message ect.
│   ├── layouts/             # for admin and super admin
│   ├── adminside/           # All admin functionalities
├── static/                  # CSS , js files 
├── manage.py                # Django CLI entry point
├── requirements.txt         # Project dependencies
```

---


## 🛠️ Setup Instructions

### 1. Prerequisites
Ensure you have the following installed:
- Python 3.8+

### 2. Clone the Repository
```bash
https://github.com/athishulleri01/TaskManagement-Noviindus.git
cd TaskManagement-Noviindus
```


### 3. Apply Migrations & Create Superuser
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 🔥 Access Admin Dashboard

[http://127.0.0.1:8000/api/v1/admin/super_admin_dash/](http://127.0.0.1:8000/api/v1/admin/super_admin_dash/)


## 🔥 Redoc Doccumentation

[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc/)



### ✅ Admin Panel (Custom HTML Templates)
#### 👑 SuperAdmin Capabilities
- Manage users and admins (create, delete, assign roles).
- Assign users to admins.
- View all tasks and completion reports.

#### 🛠️ Admin Capabilities
- Assign tasks to users.
- View and manage tasks and reports for their users.

#### 👤 User Capabilities
- View and update assigned tasks.
- Submit completion reports and worked hours.
  
### Roles and Permissions

| Role       | Permissions                                                                 |
|------------|-----------------------------------------------------------------------------|
| SuperAdmin | Full user/admin/task management, full report access                         |
| Admin      | Task management for assigned users, report view access                      |
| User       | View/update own tasks, submit reports and worked hours                     |




## 🔥 API Endpoints


### 🟢 **User Registration**
#### **POST** `/api/v1/auth/users/`
**Request:**
```json
{
  "username": "athishulleri",
  "name": "athish",
  "mobile": "7076464508",
  "email": "athishulleri@gmail.com",
  "password": "Athish@123",
  "re_password": "Athish@123"
}
```
**Response:**
```json
{
    "name": "athish",
    "mobile": "7076464508",
    "email": "athishulleri@gmail.com",
    "username": "athishulleri",
    "id": "9c5bc472-6241-454e-b964-7ee8f2c34b8a"
}
```
---

### 🟢 **Obtain Access & Refresh Tokens (Login)**
#### **POST** `/api/v1/auth/login/`
**Request:**
```json
{
  "username": "username",
  "password": "yourpassword"
}
```
**Response:**
```json
{
  "message": "Login Successful."
}
```
---

### 🟢 **Refresh Access Token**
#### **POST** `/api/v1/auth/refresh/`
(No body required, uses refresh token from cookies)
**Response:**
```json
{
  "message": "Access tokens refreshed successfully"
}
```

---

### 🟢 **View asigned task **
#### **GET** `/api/v1/tasks/`
(No body required, uses access token)
**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "title": "demo",
            "description": "demo decription",
            "due_date": "2025-05-25",
            "status": "in_progress",
            "completion_report": "hfa",
            "worked_hours": "2.00",
            "created_at": "2025-05-02T11:25:17.160027Z",
            "updated_at": "2025-05-02T13:14:12.350765Z",
            "assigned_to": 35
        },
       
    ]
}
```

---

### 🟢 **Update asigned task **
#### **PUT** `/api/v1/tasks/{id}/`
(body required, uses access token)
**Request:**
```json
{
"status": "completed",
"completion_report": "....",
"worked_hours": "2"
}
```
**Response:**
```json
{
    "status": "completed",
    "completion_report": "....",
    "worked_hours": "2.00"
}
```

---


## 💾 Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite
- **Authentication**: JWT (JSON Web Token)
- **Frontend**: Custom HTML templates (for Admin panel)

## 📦 Requirements

Ensure your `requirements.txt` includes:
- Django
- djangorestframework
- djangorestframework-simplejwt

---

