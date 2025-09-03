# # app/api/attendance_analysis.py

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from app.db.database import approved_students,otps,attendance
from app.core.config import SUBJECTS




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

    subjects = SUBJECTS[program][branch][semester]

    if subject:
        if subject not in subjects:
            raise HTTPException(status_code=400, detail=f"Subject '{subject}' not in student curriculum")
        subjects = [subject]

    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    result = {sub: {"attended": 0, "total": 0, "percentage": 0} for sub in subjects}

    # Count total classes
    for otp_doc in otps.find({
        "subject": {"$in": subjects},
        "start_time": {"$gte": start_date, "$lt": end_date}
    }):
        sub = otp_doc["subject"]
        if sub in result:
            result[sub]["total"] += 1

    # Count attended classes
    for att_doc in attendance.find({
        "roll_no": roll_no,
        "subject": {"$in": subjects},
        "marked_at": {"$gte": start_date, "$lt": end_date}
    }):
        sub = att_doc["subject"]
        if sub in result:
            result[sub]["attended"] += 1

    total_classes = sum(stats["total"] for stats in result.values())
    total_attended = sum(stats["attended"] for stats in result.values())

    for stats in result.values():
        if stats["total"] > 0:
            stats["percentage"] = round((stats["attended"] / stats["total"]) * 100, 2)

    overall_percentage = round((total_attended / total_classes) * 100, 2) if total_classes > 0 else 0

    return {
        "roll_no": roll_no,
        "branch": branch,
        "semester": semester,
        "month": f"{start_date.strftime('%B')} {year}",
        "subject_filter": subject if subject else "All Subjects",
        "overall": {
            "attended": total_attended,
            "total": total_classes,
            "percentage": overall_percentage
        },
        "subjects": result
    }
