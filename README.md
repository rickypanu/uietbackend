# SmartPresence Backend

SmartPresence Backend handles all **server-side operations** for the SmartPresence attendance system, including user management, OTP generation, attendance tracking, notifications, and face recognition verification.


## 📌 Table of Contents

* Introduction
* Features
* Technology Stack
* System Architecture
* Setup Instructions
* API Endpoints
* Demo
* Future Improvements
* Team



## 📝 Introduction

The backend of SmartPresence ensures:

* **Automated attendance processing** via OTP and face recognition
* **Secure role-based access** for students, teachers, and admin
* **Real-time notifications** and attendance history
* **Scalable and modular design** for easy future enhancements

## ✨ Features

* Role-based user registration, login, and approval
* OTP generation & validation
* Attendance tracking and reporting
* Notifications management
* Face recognition verification
* Admin approval workflow
* Database management with MongoDB Atlas



## 🛠 Technology Stack

* **Python 3.10+** – Programming language
* **FastAPI** – Backend framework
* **MongoDB Atlas** – Database
* **OpenCV & `face_recognition`** – Face recognition
* **Pydantic** – Data validation
* **Uvicorn** – ASGI server for running FastAPI

---

## 🏗 System Architecture

```
           ┌─────────────────────────┐
           │       React Frontend    │
           │ - Student/Teacher/Admin│
           │ - Dashboards           │
           │ - OTP & Face UI        │
           └─────────┬──────────────┘
                     │ HTTP / REST API
                     ▼
           ┌─────────────────────────┐
           │     FastAPI Backend     │
           │ - User Management       │
           │ - OTP Generation        │
           │ - Attendance Logic      │
           │ - Notifications         │
           │ - Face Recognition API  │
           └─────────┬──────────────┘
                     │
                     ▼
           ┌─────────────────────────┐
           │      MongoDB Atlas      │
           │ - Users Collection      │
           │ - OTPs Collection       │
           │ - Attendance Records    │
           │ - Notifications         │
           └─────────────────────────┘
```

### Flow Details

1. **User Registration/Login**

   * Users register as student/teacher via frontend.
   * Backend validates and stores data in MongoDB.
   * Admin approval is required before access.

2. **OTP-Based Attendance**

   * Teacher generates OTP for class.
   * OTP stored in backend database.
   * Student submits OTP; backend validates and marks attendance.

3. **Face Recognition Attendance (Optional)**

   * Frontend captures student image.
   * Backend compares image with stored face encodings.
   * Attendance is marked if face matches.

4. **Notifications System**

   * Teachers send notifications via API.
   * Stored in MongoDB; students fetch in real-time.

5. **Admin Module**

   * Approves/rejects users, manages attendance and notifications.
   * All changes reflected in the database.

---

## ⚙️ Setup Instructions

```bash
# Clone repository
git clone https://github.com/your-backend-link
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Example .env file:
# MONGO_URI=<your-mongodb-uri>
# SECRET_KEY=<your-secret-key>

# Run backend server
uvicorn app.main:app --reload
```

> Make sure the **frontend is running** to interact with the backend APIs.

---

## 🔗 API Endpoints

| Endpoint              | Method          | Description                      |
| --------------------- | --------------- | -------------------------------- |
| `/register`           | POST            | Register student/teacher         |
| `/login`              | POST            | User login                       |
| `/generate-otp`       | POST            | Teacher generates OTP            |
| `/mark-attendance`    | POST            | Student marks attendance         |
| `/attendance-history` | GET             | Fetch attendance records         |
| `/notifications`      | POST/GET/DELETE | Manage notifications             |
| `/upload-face`        | POST            | Upload face encoding for student |
| `/approve-user`       | POST            | Admin approves registration      |


## 🔮 Future Improvements

* Integration with SMS/email alerts
* AI-based attendance analytics
* Support for multiple campuses or branches
* Biometric verification (fingerprint/iris)
* Role-based dashboards in admin panel



## 👨‍💻 Team

* **Team Name:** Innovators+
* Members: 1. Ritik Chauhan 2. Ricky Panu 3. Priyanshu Kaushik 4. Mohit Kumar 5.Harsha GUpta 6. Hritk Pundir



