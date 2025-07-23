from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.config import ADMIN_ID, ADMIN_PASSWORD, ADMIN_EMAIL, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.db.database import (
    pending_students, approved_students, rejected_students,
    pending_teachers, approved_teachers, rejected_teachers
)
from app.core.email_utils import send_email
from datetime import datetime, timedelta
from jose import jwt
import random
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
import os
router = APIRouter()

# TEMPORARY: in-memory; use Redis/DB in production
admin_otp_store = {}
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

class AdminLogin(BaseModel):
    user_id: str
    password: str

class OtpVerify(BaseModel):
    user_id: str
    otp: str

@router.post("/admin/request-otp")
def admin_request_otp(data: AdminLogin):
    if data.user_id != ADMIN_ID or data.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    
    otp = str(random.randint(100000, 999999))
    expires = datetime.utcnow() + timedelta(minutes=5)
    admin_otp_store[data.user_id] = {"otp": otp, "expires": expires}

    subject = "Your Admin Login OTP"
    message = f"""
    Hello Admin,
    Your OTP to login to the Admin Dashboard is: {otp}
    It is valid for 5 minutes.
    If you did not request this, please contact support immediately.
    Regards
    Geeky_coders
    """

    send_email(ADMIN_EMAIL, subject, message)
    return {"message": "OTP sent to admin email"}


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/admin/verify-otp")
def admin_verify_otp(data: OtpVerify):
    record = admin_otp_store.get(data.user_id)
    if not record:
        raise HTTPException(status_code=400, detail="No OTP requested")
    if datetime.utcnow() > record["expires"]:
        raise HTTPException(status_code=400, detail="OTP expired")
    if record["otp"] != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # OTP valid → delete it
    del admin_otp_store[data.user_id]

    access_token = create_access_token({"sub": data.user_id})
    return {"access_token": access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/verify-otp")

def verify_admin_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("sub").lower() != ADMIN_ID.lower():
            raise HTTPException(status_code=403, detail="Invalid admin token")
        return payload  # This was missing
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid admin token")

    
@router.post("/admin/login")
def admin_login(data: AdminLogin):
    if data.user_id != ADMIN_ID or data.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    return {"message": "Admin login successful"}

@router.post("/admin/approve/student/{roll_no}")

def approve_student(roll_no: str, admin_payload: dict = Depends(verify_admin_token)):
    # student = pending_students.find_one({"roll_no": roll_no})
    student = pending_students.find_one({"roll_no": {"$regex": f"^{roll_no}$", "$options": "i"}})


    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    pending_students.delete_one({"roll_no": roll_no})
    approved_students.insert_one(student)
    name = student["full_name"]
    email = student["email"]
    subject = "Your account has been approved! 🎉"
    message = f"""
    Dear {name},

    We are pleased to inform you that your student account has been successfully approved on the College Attendance Management System.

    You may now log in to your account and make use of the following features:
    - Mark your attendance using the provided OTP system  
    - View your attendance history at any time  
    - Stay informed about class schedules and important updates

    Should you have any questions or require assistance, please do not hesitate to contact the system administrator or visit the relevant department office.
    We welcome you to the platform and wish you a successful academic journey.

    Best regards,  
    College Attendance Team
    """

    send_email(email, subject, message)
    return {"message": "Student approved"}

@router.post("/admin/reject/student/{roll_no}")
def reject_student(roll_no: str, admin_payload: dict = Depends(verify_admin_token)):
    # student = pending_students.find_one({"roll_no": roll_no})
    student = pending_students.find_one({"roll_no": {"$regex": f"^{roll_no}$", "$options": "i"}})

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    pending_students.delete_one({"roll_no": roll_no})
    rejected_students.insert_one(student)
    name = student["full_name"]
    email = student["email"]
    subject = "Update on Your Student Account Registration"
    message = f"""
    Dear {name},

    Thank you for registering on our College Attendance Management System.
    We regret to inform you that your registration could not be approved at this time due to certain issues or discrepancies identified during the verification process.
    If you believe this is an error or if you require further clarification, please contact the college administration or visit the department office responsible for student registration.

    We appreciate your understanding and cooperation.

    Best regards,  
    College Attendance Team
    """

    send_email(email, subject, message)
    return {"message": "Student rejected"}

# same for teacher
@router.post("/admin/approve/teacher/{employee_id}")
def approve_teacher(employee_id: str, admin_payload: dict = Depends(verify_admin_token)):
    emp_id = employee_id.upper()
    # teacher = pending_teachers.find_one({"employee_id": emp_id})
    teacher = pending_teachers.find_one({"employee_id": {"$regex": f"^{emp_id}$", "$options": "i"}})

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    pending_teachers.delete_one({"employee_id": emp_id})
    approved_teachers.insert_one(teacher)
    name = teacher["full_name"]
    email = teacher["email"]
    subject = "Your Teacher Account Has Been Approved!"
    message = f"""
    Dear {name},

    We are pleased to inform you that your teacher account has been successfully approved on the College Attendance Management System.

    You may now log in to your account and access the following features:
    - Generate and manage OTP-based attendance  
    - View your attendance history  
    - Stay informed about class activities and updates

    If you have any questions or require assistance, please do not hesitate to contact the system administrator or support team.

    Welcome aboard, and thank you for being a part of our academic community.

    Best regards,  
    College Attendance Team
    """

    send_email(email, subject, message)
    return {"message": "Teacher approved"}

@router.post("/admin/reject/teacher/{employee_id}")
def reject_teacher(employee_id: str, admin_payload: dict = Depends(verify_admin_token)):
    emp_id = employee_id.upper()
    # teacher = pending_teachers.find_one({"employee_id": emp_id})
    teacher = pending_teachers.find_one({"employee_id": {"$regex": f"^{emp_id}$", "$options": "i"}})

    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    pending_teachers.delete_one({"employee_id": emp_id})
    rejected_teachers.insert_one(teacher)
    name = teacher["full_name"]
    email = teacher["email"]
    subject = "Update on Your Teacher Account Registration"
    message = f"""
    Dear {name},

    Thank you for registering on our College Attendance Management System.

    We regret to inform you that your registration could not be approved at this time due to certain issues or discrepancies identified during the verification process.

    If you believe this is an error or if you require further clarification, please contact the college administration or visit the department office responsible for teacher registration.

    We appreciate your understanding and cooperation.

    Best regards,  
    College Attendance Team

    """

    send_email(email, subject, message)
    return {"message": "Teacher rejected"}

# lists
@router.get("/admin/list/pending/students")
def list_pending_students():
    return list(pending_students.find({}, {"_id": 0}))

@router.get("/admin/list/pending/teachers")
def list_pending_teachers():
    return list(pending_teachers.find({}, {"_id": 0}))

@router.get("/admin/list/approved/students")
def list_approved_students():
    return list(approved_students.find({}, {"_id": 0}))

@router.get("/admin/list/approved/teachers")
def list_approved_teachers():
    return list(approved_teachers.find({}, {"_id": 0}))

@router.get("/admin/list/rejected/students")
def list_rejected_students():
    return list(rejected_students.find({}, {"_id": 0}))

@router.get("/admin/list/rejected/teachers")
def list_rejected_teachers():
    return list(rejected_teachers.find({}, {"_id": 0}))
