# # app/api/attendance_analysis.py

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from app.db.database import approved_students,otps,attendance
from app.core.config import SUBJECTS
from bson import ObjectId
from datetime import datetime



router = APIRouter()

@router.get("/attendance-analysis/{roll_no}")
def student_attendance_analysis(
    roll_no: str,
    month: int,
    year: int,
    subject: str = Query(None, description="Optional subject filter")
):
    roll_no = str(roll_no)

    # 1. Get student info
    student = approved_students.find_one({"roll_no": roll_no})
    if not student:
        raise HTTPException(status_code=404, detail=f"Student with roll_no {roll_no} not found")

    program = "BE"
    branch = student.get("branch")
    semester = str(student.get("semester"))

    if program not in SUBJECTS or branch not in SUBJECTS[program] or semester not in SUBJECTS[program][branch]:
        raise HTTPException(status_code=400, detail="Subjects not defined for this branch/semester")

    # curriculum subjects (normalize to lowercase for DB queries)
    subjects = [s.lower() for s in SUBJECTS[program][branch][semester]]

    # if specific subject filter is provided
    if subject:
        if subject.lower() not in subjects:
            raise HTTPException(status_code=400, detail=f"Subject '{subject}' not in student curriculum")
        subjects = [subject.lower()]

    start_date = datetime(year, month, 1)
    end_date = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

    # Initialize result
    result = {s.upper(): {"attended": 0, "total": 0, "percentage": 0} for s in subjects}

    # Count total classes (case-insensitive match)
    otp_query = {
        "start_time": {"$gte": start_date, "$lt": end_date},
        "$or": [{"subject": {"$regex": f"^{s}$", "$options": "i"}} for s in subjects]
    }
    for otp_doc in otps.find(otp_query):
        sub = otp_doc["subject"].lower()
        if sub in subjects:
            result[sub.upper()]["total"] += 1

    # Count attended classes (case-insensitive match)
    att_query = {
        "roll_no": roll_no,
        "marked_at": {"$gte": start_date, "$lt": end_date},
        "$or": [{"subject": {"$regex": f"^{s}$", "$options": "i"}} for s in subjects]
    }
    for att_doc in attendance.find(att_query):
        sub = att_doc["subject"].lower()
        if sub in subjects:
            result[sub.upper()]["attended"] += 1

    # Debug sample
    att_sample = attendance.find_one({"roll_no": roll_no})
    print("Sample attendance:", att_sample, type(att_sample.get("marked_at")))

    # Totals
    total_classes = sum(stats["total"] for stats in result.values())
    total_attended = sum(stats["attended"] for stats in result.values())
    print("total_attended", total_attended)
    print("total class", total_classes)

    # Percentages
    for stats in result.values():
        if stats["total"] > 0:
            stats["percentage"] = round((stats["attended"] / stats["total"]) * 100, 2)

    overall_percentage = round((total_attended / total_classes) * 100, 2) if total_classes > 0 else 0

    return {
        "roll_no": roll_no,
        "branch": branch,
        "semester": semester,
        "month": f"{start_date.strftime('%B')} {year}",
        "subject_filter": subject.upper() if subject else "All Subjects",
        "overall": {
            "attended": total_attended,
            "total": total_classes,
            "percentage": overall_percentage
        },
        "subjects": result
    }
