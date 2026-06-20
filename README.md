# LegalConnect – Lawyer & Client Case Management System

## Overview

LegalConnect is a web-based legal case management platform designed to bridge the gap between clients and lawyers. The system allows users to register, authenticate securely using JWT tokens, file legal complaints, manage cases, track hearing dates, and maintain case-related notes through an intuitive Streamlit interface backed by a FastAPI REST API.

The platform uses PostgreSQL for data storage, FastAPI for backend services, JWT-based authentication for security, and Streamlit for the frontend dashboard.

---

# Project Structure

```text
LegalConnect/
│
├── app/
│   ├── auth/
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   └── security.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── complaint.py
│   │   └── case.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── complaints.py
│   │   ├── cases.py
│   │   └── chat.py
│   │
│   └── schemas/
│       ├── user.py
│       ├── complaint.py
│       └── case.py
│
├── main.py
├── streamlit_app.py
├── requirements.txt
├── .env
├── README.md
└── venv/
```

---

# Features

### User Authentication

* User Registration
* User Login
* JWT Access Tokens
* Role-based Access (Client / Lawyer)
* Password Hashing using Bcrypt

### Complaint Management

* Create Legal Complaints
* Categorize Complaints
* Set Complaint Urgency
* Assign Preferred Lawyer

### Case Management

* Create Cases
* View Existing Cases
* Update Case Status
* Update Hearing Dates
* Maintain Case Notes

### User Dashboard

* Streamlit-based Interactive Interface
* Secure API Communication
* Complaint Tracking
* Case Monitoring

---

# Technology Stack

## Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* JWT Authentication
* Passlib (Bcrypt)
* Python-Jose

## Frontend

* Streamlit
* Requests
* Pandas

## Database

* PostgreSQL

---

# Setting Up the Virtual Environment

Open terminal inside the project directory:

```bash
python -m venv venv
```

Activate the environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

# Installing Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

Additional packages used in the project:

```bash
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-jose[cryptography]
passlib[bcrypt]
python-multipart
streamlit
pandas
requests
```

---

# PostgreSQL Configuration

Create a PostgreSQL database:

```sql
CREATE DATABASE legalconnect;
```

Configure the `.env` file:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5433/legalconnect

JWT_SECRET_KEY=your_secret_key
JWT_REFRESH_SECRET_KEY=your_refresh_secret

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Password Hashing

Passwords are never stored in plain text.

```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    return pwd_context.verify(
        password,
        hashed_password
    )
```

---

# JWT Authentication

JWT tokens are generated during login and attached to subsequent requests.

```python
def create_access_token(email, role):
    payload = {
        "sub": email,
        "role": role
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )
```

JWT Authentication enables:

* Secure User Sessions
* Role-Based Authorization
* Protected Endpoints
* Token Verification

---

# Running the Backend

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

---

# Running the Frontend

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

---

# Workflow

### Client

1. Register Account
2. Login
3. Create Complaint
4. Track Complaint Status
5. View Assigned Cases

### Lawyer

1. Register/Login
2. View Cases
3. Update Case Status
4. Schedule Hearings
5. Maintain Case Notes

---

# API Modules

## Authentication

```text
POST /auth/auth/signup
POST /auth/auth/login
POST /auth/auth/refresh
GET  /auth/auth/me
```

## Complaints

```text
POST /complaints/
GET  /complaints/
```

## Cases

```text
GET    /cases/
POST   /cases/
GET    /cases/{case_id}
DELETE /cases/{case_id}
PUT    /cases/{case_id}/status
PUT    /cases/{case_id}/hearing
PUT    /cases/{case_id}/notes
```

---

# Future Enhancements

* Lawyer Recommendation System
* AI-Based Legal Assistant
* Document Upload & Verification
* Email Notifications
* Hearing Reminders
* Real-Time Chat System
* Legal Document Generation
* Analytics Dashboard

---

# Authors
Surabhi Nare, Sejal Mahangare, Zoya Pathan

GitHub Profiles:
- https://github.com/surabhinare21-eng
- https://github.com/sage-2102
- https://github.com/zoyapathan
  
Developed as a Legal Case Management Platform using FastAPI, PostgreSQL, JWT Authentication, and Streamlit.
