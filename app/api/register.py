from fastapi import APIRouter, HTTPException
from app.schemas.student import StudentRegister
from app.schemas.teacher import TeacherRegister
from app.db.database import (
    pending_students, approved_students, rejected_students,
    pending_teachers, approved_teachers, rejected_teachers
)

router = APIRouter()

def check_existing_user(field_name: str, value: str, collections: list):
    for collection, status in collections:
        if collection.find_one({field_name: value}):
            return status
    return None

@router.post("/register/student")
def register_student(student: StudentRegister):
    student_data = student.dict()
    student_data['dob'] = student_data['dob'].isoformat()

    checks = [
        ('roll_no', student_data['roll_no']),
        ('phone', student_data['phone']),
        ('email', student_data['email'])
    ]

    collections = [
        (pending_students, "pending"),
        (approved_students, "approved"),
        (rejected_students, "rejected")
    ]

    for field, value in checks:
        status = check_existing_user(field, value, collections)
        if status == "pending":
            raise HTTPException(
                status_code=400,
                detail=f"A registration request with this {field.replace('_', ' ')} is already pending. Please await verification."
            )
        elif status == "approved":
            raise HTTPException(
                status_code=400,
                detail=f"This {field.replace('_', ' ')} has already been approved. Please log in using your credentials."
            )
        elif status == "rejected":
            raise HTTPException(
                status_code=400,
                detail=f"Registration using this {field.replace('_', ' ')} was previously rejected. Kindly contact the administrator for assistance."
            )

    pending_students.insert_one(student_data)
    return {
        "message": f"Registration request submitted successfully for {student_data['full_name']} (Roll No: {student_data['roll_no']}). Please await verification."
    }


@router.post("/register/teacher")
def register_teacher(teacher: TeacherRegister):
    teacher_data = teacher.dict()
    teacher_data["dob"] = teacher_data["dob"].isoformat()

    employee_id = teacher_data["employee_id"]
    email = teacher_data["email"]
    phone = teacher_data["phone"]

    # Check for duplicate employee_id
    if (
        pending_teachers.find_one({"employee_id": employee_id}) or
        approved_teachers.find_one({"employee_id": employee_id}) or
        rejected_teachers.find_one({"employee_id": employee_id})
    ):
        raise HTTPException(
            status_code=400,
            detail="An account with this Employee ID already exists or has a pending/rejected registration."
        )

    # Check for duplicate email
    if (
        pending_teachers.find_one({"email": email}) or
        approved_teachers.find_one({"email": email}) or
        rejected_teachers.find_one({"email": email})
    ):
        raise HTTPException(
            status_code=400,
            detail="This email address is already registered or has a pending/rejected registration."
        )

    # Check for duplicate phone number
    if (
        pending_teachers.find_one({"phone": phone}) or
        approved_teachers.find_one({"phone": phone}) or
        rejected_teachers.find_one({"phone": phone})
    ):
        raise HTTPException(
            status_code=400,
            detail="This phone number is already registered or has a pending/rejected registration."
        )

    # Insert registration request
    pending_teachers.insert_one(teacher_data)
    return {
        "message": f"Registration request submitted successfully for {teacher_data['full_name']} (Employee ID: {employee_id}). Please await verification."
    }
