from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId
from typing import List, Optional
from app.db.database import classes, approved_students, attendance,otps  # imported collections

router = APIRouter(
    prefix="/classes",
    tags=["Classes"]
)

# ------------------------------
# Models
# ------------------------------
class ClassCreate(BaseModel):
    teacher_id: str
    department: str
    course: str
    branch: str
    section: str
    semester: int
    subject: str


class ClassResponse(BaseModel):
    id: str
    teacher_id: str
    department: str
    course: str
    branch: str
    section: str
    semester: int
    subject: str
    created_at: datetime


# ------------------------------
# Routes
# ------------------------------

@router.post("/create", response_model=ClassResponse)
def create_class(class_data: ClassCreate):
    """
    Teacher creates a new class
    """
    class_id = str(ObjectId())

    new_class = {
        "_id": class_id,
        "teacher_id": class_data.teacher_id,
        "department": class_data.department,
        "course": class_data.course,
        "branch": class_data.branch,
        "section": class_data.section,
        "semester": class_data.semester,
        "subject": class_data.subject,
        "created_at": datetime.utcnow()
    }

    result = classes.insert_one(new_class)  # ✅ no await here
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Class creation failed")

    return {
        "id": class_id,
        **class_data.dict(),
        "created_at": new_class["created_at"]
    }


# @router.get("/list/{teacher_id}", response_model=List[ClassResponse])
# def list_classes(teacher_id: str):
#     """
#     List all classes created by a teacher
#     """
#     result = list(classes.find({"teacher_id": teacher_id}))
#     return [
#         {
#             "id": str(c["_id"]),
#             "teacher_id": c["teacher_id"],
#             "department": c["department"],
#             "course": c["course"],
#             "branch": c["branch"],
#             "section": c["section"],
#             "semester": c["semester"],
#             "subject": c["subject"],
#             "created_at": c["created_at"]
#         }
#         for c in result
#     ]

@router.get("/list/{teacher_id}", response_model=List[ClassResponse])
def list_classes(teacher_id: str):
    """
    List all classes created by a teacher
    """
    result = list(classes.find({"teacher_id": teacher_id}))
    return [
        {
            "id": str(c.get("_id")),
            "teacher_id": c.get("teacher_id", ""),
            "department": c.get("department", ""),
            "course": c.get("course", ""),      # <-- safe
            "branch": c.get("branch", ""),
            "section": c.get("section", ""),
            "semester": c.get("semester", ""),
            "subject": c.get("subject", ""),
            "created_at": c.get("created_at", None),
        }
        for c in result
    ]




@router.get("/register/{class_id}")
def get_class_register(
    class_id: str,
    month: Optional[int] = None,   # ✅ filter month
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    # 1. Get class info
    class_data = classes.find_one({"_id": class_id})
    if not class_data:
        raise HTTPException(status_code=404, detail="Class not found")

    # 2. Get students
    students = list(
        approved_students.find(
            {
                "course": class_data["course"],
                "branch": class_data["branch"],
                "section": class_data["section"],
                "semester": class_data["semester"]
            },
            {"_id": 0, "roll_no": 1, "name": 1, "full_name": 1}
        ).sort("roll_no", 1)
    )
    for s in students:
        if "full_name" not in s and "name" in s:
            s["full_name"] = s["name"]

    # 3. Get OTPs (lectures)
    otp_query = {"teacher_id": class_data["teacher_id"], "subject": class_data["subject"]}
    otp_docs = list(otps.find(otp_query, {"_id": 0, "otp": 1, "start_time": 1}))

    otp_dates = []
    for o in otp_docs:
        if "start_time" in o:
            date_str = o["start_time"].strftime("%Y-%m-%d")
            month_int = int(date_str.split("-")[1])
            # ✅ Apply month filter
            if month and month_int != month:
                continue
            # ✅ Apply date range filter
            if start_date and end_date:
                if not (start_date <= date_str <= end_date):
                    continue
            otp_dates.append({"otp": o["otp"], "date": date_str})

    otp_dates.sort(key=lambda x: x["date"])
    date_list = [d["date"] for d in otp_dates]

    # 4. Attendance records
    otp_values = [d["otp"] for d in otp_dates]
    attendance_records = list(
        attendance.find(
            {"otp": {"$in": otp_values}},
            {"_id": 0, "roll_no": 1, "otp": 1, "status": 1}
        )
    )

    attendance_lookup = {}
    for r in attendance_records:
        roll = r["roll_no"]
        otp_val = r["otp"]
        status = r.get("status", "Present")
        if roll not in attendance_lookup:
            attendance_lookup[roll] = {}
        attendance_lookup[roll][otp_val] = status

    # 5. Build register
    student_register = []
    for s in students:
        roll_no = s["roll_no"]
        row = {
            "roll_no": roll_no,
            "name": s["full_name"],
            "attendance": {},
            "total_present": 0,
            "total_classes": len(date_list),
            "percentage": "0%"
        }

        present_count = 0
        for d in otp_dates:
            otp_val = d["otp"]
            date_val = d["date"]
            if roll_no in attendance_lookup and otp_val in attendance_lookup[roll_no]:
                row["attendance"][date_val] = "P"
                present_count += 1
            else:
                row["attendance"][date_val] = "A"

        row["total_present"] = present_count
        if len(date_list) > 0:
            row["percentage"] = f"{(present_count / len(date_list) * 100):.1f}%"

        student_register.append(row)

    return {
        "class_info": {
            "department":class_data["department"],
            "course":class_data["course"],
            "branch": class_data["branch"],
            "semester": class_data["semester"],
            "section": class_data["section"],
            "subject": class_data["subject"],
        },
        "dates": date_list,
        "students": student_register
    }


@router.delete("/{class_id}")
def delete_class(class_id: str):
    """
    Delete a class by its ID.
    Also optionally, you can delete related OTPs and attendance records.
    """
    # 1️⃣ Check if class exists
    class_data = classes.find_one({"_id": class_id})
    if not class_data:
        raise HTTPException(status_code=404, detail="Class not found")

    # 2️⃣ Delete the class
    result = classes.delete_one({"_id": class_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete class")

    # # 3️⃣ Optionally delete related OTPs
    # otps.delete_many({"teacher_id": class_data["teacher_id"], "subject": class_data["subject"]})

    # # 4️⃣ Optionally delete related attendance records
    # attendance.delete_many({"otp": {"$in": [o["otp"] for o in otps.find({"teacher_id": class_data["teacher_id"], "subject": class_data["subject"]}, {"_id": 0, "otp": 1})]}})

    return {"message": "Class and related records deleted successfully"}