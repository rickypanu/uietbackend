# app/api/student.py
from fastapi import APIRouter, HTTPException, UploadFile, File 
from app.db.database import otps, attendance, approved_students, approved_teachers, notifications
from app.core.config import SUBJECTS
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from io import StringIO
import csv
import pytz
import math
from typing import Optional
import base64
from datetime import date, timedelta, datetime

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

router = APIRouter()

IST = pytz.timezone('Asia/Kolkata')

class MarkAttendanceRequest(BaseModel):
    roll_no: str
    otp: str
    subject: str
    visitorId: str
    lat: Optional[float]
    lng: Optional[float]



class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    branch: Optional[str] = None
    section: Optional[str] = None
    semester: Optional[int] = None
    dob: Optional[date] = None

@router.post("/student/markAttendance")
def mark_attendance(req: MarkAttendanceRequest):
    roll_no = req.roll_no.upper()
    otp = req.otp
    subject = req.subject.strip().lower()
    visitor_id = req.visitorId

    SUBJECTS_LOWER = [s.lower() for s in SUBJECTS]
    # if subject not in SUBJECTS_LOWER:
    #     raise HTTPException(status_code=400, detail="Invalid subject")

    student = approved_students.find_one({"roll_no": roll_no})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    otp_doc = otps.find_one({"otp": otp})
    if not otp_doc:
        raise HTTPException(status_code=404, detail="Invalid OTP")

    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)

    start_time = otp_doc["start_time"]
    end_time = otp_doc["end_time"]

    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=pytz.utc)
        
    if end_time.tzinfo is None:
        end_time = end_time.replace(tzinfo=pytz.utc)

    if not (start_time <= now_utc <= end_time):
        raise HTTPException(status_code=400, detail="OTP expired or not active")

    if otp_doc["subject"].strip().lower() != subject:
        raise HTTPException(status_code=400, detail="Subject does not match OTP")

    already_marked = attendance.find_one({"roll_no": roll_no, "otp": otp})
    if already_marked:
        raise HTTPException(status_code=400, detail="Attendance already marked")

    # ✅ location validation
    if req.lat is None or req.lng is None:
        raise HTTPException(status_code=400, detail="Location (lat/lng) required to mark attendance")

    location = otp_doc.get("location")
    if not location or "lat" not in location or "lng" not in location:
        raise HTTPException(status_code=500, detail="Teacher location not available in OTP")

    teacher_lat = location["lat"]
    teacher_lng = location["lng"]
    print("Student location:", req.lat, req.lng)
    print("Teacher location:", teacher_lat, teacher_lng)

    distance = haversine_distance(req.lat, req.lng, teacher_lat, teacher_lng)
    if distance > 100:
        raise HTTPException(status_code=400, detail=f"Too far from teacher's location ({round(distance)} m > 100 m)")

    # ✅ recent device check
    from datetime import timedelta
    fifty_min_ago = now_utc - timedelta(minutes=50)
    recent = attendance.find_one({
        # "roll_no": roll_no,
        "visitor_id": visitor_id,
        "marked_at": {"$gte": fifty_min_ago}
    })
    if recent:
        raise HTTPException(status_code=400, detail="Attendance already marked from this device recently")
        # raise HTTPException(status_code=400, detail="Attendance already marked from this device recently (within 50 minutes)")


    attendance.insert_one({
        "roll_no": roll_no,
        "student_name": student["full_name"],
        "subject": subject,
        "otp": otp,
        "visitor_id": visitor_id,
        "marked_at": now_utc,
        "lat": req.lat,
        "lng": req.lng
    })

    return {"message": "Attendance marked successfully"}


@router.get("/student/view-attendance/{roll_no}")
def view_attendance(roll_no: str, subject: str = None):
    roll_no = roll_no.upper()
    query = {"roll_no": roll_no}

    if subject:
        subject = subject.strip().lower()
        SUBJECTS_LOWER = [s.lower() for s in SUBJECTS]
        if subject not in SUBJECTS_LOWER:
            raise HTTPException(status_code=400, detail="Invalid subject")
        query["subject"] = subject

    records = list(attendance.find(query))

    result = []
    for r in records:
        marked_at = r.get("marked_at")
        if marked_at and marked_at.tzinfo is None:
            marked_at = marked_at.replace(tzinfo=pytz.utc)
        marked_at_ist = marked_at.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S") if marked_at else None

        result.append({
            "subject": r["subject"],
            "marked_at": marked_at_ist
        })

    return result

@router.get("/student/check-otp/{otp}")
def check_otp(otp: str):
    otp_doc = otps.find_one({"otp": otp})
    if not otp_doc:
        raise HTTPException(status_code=404, detail="Invalid OTP")

    start_time = otp_doc["start_time"]
    end_time = otp_doc["end_time"]

    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=pytz.utc)
    if end_time.tzinfo is None:
        end_time = end_time.replace(tzinfo=pytz.utc)

    return {
        "subject": otp_doc["subject"],
        "start_time": start_time.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S")
    }

@router.get("/student/export-attendance/{roll_no}")
async def export_attendance_csv(roll_no: str):
    roll_no = roll_no.upper()
    records = list(attendance.find({"roll_no": roll_no}))

    if not records:
        raise HTTPException(status_code=404, detail="No attendance records found.")

    csv_file = StringIO()
    writer = csv.writer(csv_file)
    writer.writerow(["Subject", "Marked At (IST)"])

    for rec in records:
        subject = rec.get("subject", "")
        marked_at = rec.get("marked_at")
        if marked_at and marked_at.tzinfo is None:
            marked_at = marked_at.replace(tzinfo=pytz.utc)
        marked_at_ist = marked_at.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S") if marked_at else ""

        writer.writerow([subject, marked_at_ist])

    csv_file.seek(0)

    filename = f"attendance_{roll_no}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        csv_file,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/student/profile/{roll_no}")
def get_student_profile(roll_no: str):
    roll_no = roll_no.upper()
    student = approved_students.find_one({"roll_no": roll_no})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # return only required fields (never return sensitive info)
    return {
        "full_name": student.get("full_name"),
        "email": student.get("email"),
        "department": student.get("department"),
        "dob": student.get("dob"),
        "course": student.get("course"),
        "branch": student.get("branch"),
        "semester": student.get("semester"),
        "section": student.get("section"),
        "roll_no": student.get("roll_no"),
        "photo": student.get("photo")
        
        # add more fields if needed
    }

@router.get("/teacher/active-otps/{employee_id}")
def get_active_otps(employee_id: str):
    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    
    active = list(otps.find({
        "teacher_id": employee_id.upper(),
        "end_time": {"$gt": now_utc}
    }).sort("end_time", -1))

    result = []
    for o in active:
        end_time_utc = o["end_time"]
        if end_time_utc.tzinfo is None:
            end_time_utc = end_time_utc.replace(tzinfo=pytz.utc)
        end_time_ist = end_time_utc.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S")

        result.append({
            "otp": o["otp"],
            "subject": o["subject"],
            "end_time": end_time_ist
        })

    return result

@router.post("/student/profile/upload-photo/{roll_no}")
async def upload_student_photo(roll_no: str, file: UploadFile = File(...)):
    roll_no = roll_no.upper()
    student = approved_students.find_one({"roll_no": roll_no})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    

    # Convert image file to base64 string
    content = await file.read()
    encoded_str = base64.b64encode(content).decode("utf-8")
    
    # Update student profile
    approved_students.update_one(
        {"roll_no": roll_no},
        {"$set": {"photo": encoded_str}}
    )

    return {"message": "Photo uploaded successfully"}




@router.patch("/student/profile/update/{roll_no}")
async def update_student_profile(roll_no: str, update: ProfileUpdate):
    roll_no = roll_no.upper()
    student = approved_students.find_one({"roll_no": roll_no})
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_fields = {}

    # Allow updating full_name, email, branch, section
    if update.full_name is not None:
        update_fields["full_name"] = update.full_name.strip()

    if update.email is not None:
        update_fields["email"] = update.email.strip().lower()

    if update.branch is not None:
        update_fields["branch"] = update.branch.strip()

    if update.section is not None:
        update_fields["section"] = update.section.strip().upper()

    if update.semester is not None:
        if update.semester not in range(1, 9):
            raise HTTPException(status_code=400, detail="Semester must be between 1 and 8")
        update_fields["semester"] = update.semester

    if update.dob is not None:
        update_fields["dob"] = update.dob.isoformat()

    if not update_fields:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    approved_students.update_one(
        {"roll_no": roll_no},
        {"$set": update_fields}
    )

    return {"message": "Profile updated successfully"}


@router.get("/student/notifications/{branch}/{section}/{semester}")
def get_notifications(branch: str, section: str, semester: str):
    now = datetime.utcnow()
    notifs = list(notifications.find({
        "target_branch": branch.upper(),
        "target_section": section.upper(),
        "target_semester": semester,
        "expiry_time": {"$gte": now}
    }).sort("timestamp", -1))

    results = []
    for n in notifs:
        teacher = approved_teachers.find_one({"employee_id": n["sender_id"]})
        ist_timestamp = n["timestamp"] + timedelta(hours=5, minutes=30)
        results.append({
            "message": n["message"],
            "file_url": n.get("file_url"),
            # "timestamp": n["timestamp"],
            "timestamp": ist_timestamp,
            "expiry_time": n["expiry_time"],
            "teacher_name": teacher.get("full_name", "Unknown") if teacher else "Unknown"
        })

    return results
