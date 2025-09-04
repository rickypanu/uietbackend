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

@router.get("/attendance-target/{roll_no}")
def attendance_target(
    roll_no: str,
    subject: str,
    target_percentage: float,
    from_date: str = Query(..., description="Start date in YYYY-MM-DD"),
    to_date: str = Query(None, description="End date in YYYY-MM-DD (default: today)"),
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

    subjects = [s.lower() for s in SUBJECTS[program][branch][semester]]

    if subject.lower() not in subjects:
        raise HTTPException(status_code=400, detail=f"Subject '{subject}' not in student curriculum")

    subject_key = subject.lower()
    subject_name = subject_key.upper()

    # ⏳ Convert dates
    try:
        start_date = datetime.strptime(from_date, "%Y-%m-%d")
        if to_date:
            end_date = datetime.strptime(to_date, "%Y-%m-%d")
        else:
            end_date = datetime.today()  # ✅ default to today
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    if start_date > end_date:
        raise HTTPException(status_code=400, detail="from_date cannot be after to_date")

    # 📌 Total classes in range
    total_classes = otps.count_documents({
        "subject": {"$regex": f"^{subject_key}$", "$options": "i"},
        "start_time": {"$gte": start_date, "$lte": end_date}
    })

    # 📌 Attended classes in range
    attended_classes = attendance.count_documents({
        "roll_no": roll_no,
        "subject": {"$regex": f"^{subject_key}$", "$options": "i"},
        "marked_at": {"$gte": start_date, "$lte": end_date}
    })

    current_percentage = round((attended_classes / total_classes) * 100, 2) if total_classes > 0 else 0

    if current_percentage >= target_percentage:
        return {
            "roll_no": roll_no,
            "subject": subject_name,
            "date_range": f"{from_date} → {end_date.strftime('%Y-%m-%d')}",
            "attended": attended_classes,
            "total": total_classes,
            "current_percentage": current_percentage,
            "target_percentage": target_percentage,
            "needed_classes": 0,
            "message": f"✅ You already meet or exceed {target_percentage}% attendance in {subject_name}."
        }

    # Formula: (attended + x) / (total + x) >= target%
    required = (target_percentage * total_classes - 100 * attended_classes) / (100 - target_percentage)
    required_classes = max(0, int(required) + (0 if required.is_integer() else 1))

    return {
        "roll_no": roll_no,
        "subject": subject_name,
        "date_range": f"{from_date} → {end_date.strftime('%Y-%m-%d')}",
        "attended": attended_classes,
        "total": total_classes,
        "current_percentage": current_percentage,
        "target_percentage": target_percentage,
        "needed_classes": required_classes,
        "message": f"📘 You need to attend {required_classes} more classes in {subject_name} (without bunking) to reach {target_percentage}%."
    }
