from fastapi import APIRouter, HTTPException
from app.schemas.student import StudentRegister
from app.schemas.teacher import TeacherRegister
from app.db.database import (
    pending_students, approved_students, rejected_students,
    pending_teachers, approved_teachers, rejected_teachers
)

router = APIRouter()

@router.post("/register/student")
def register_student(student: StudentRegister):
    student_data = student.dict()
    student_data['dob'] = student_data['dob'].isoformat()  # convert to string

    roll_no = student_data['roll_no']
    phone = student_data['phone']
    email = student_data['email']

    # Check in all collections if roll_no already exists
    if (
        pending_students.find_one({"roll_no": roll_no}) or
        approved_students.find_one({"roll_no": roll_no}) or
        rejected_students.find_one({"roll_no": roll_no})
    ):
        raise HTTPException(status_code=400, detail="Roll number already registered or request pending/rejected.")


    if (
        pending_students.find_one({"phone": phone}) or
        approved_students.find_one({"phone": phone}) or
        rejected_students.find_one({"phone": phone})
    ):
        raise HTTPException(status_code=400, detail="Phone number already registered or request pending/rejected.")

    if (
        pending_students.find_one({"email": email}) or
        approved_students.find_one({"email": email}) or
        rejected_students.find_one({"email": email})
    ):
        raise HTTPException(status_code=400, detail="Email already registered or request pending/rejected.")

    pending_students.insert_one(student_data)
    return {"message": "Registration request submitted"}

@router.post("/register/teacher")
def register_teacher(teacher: TeacherRegister):
    teacher_data = teacher.dict()
    teacher_data['dob'] = teacher_data['dob'].isoformat()

    employee_id = teacher_data['employee_id']

    # Check in all collections if employee_id already exists
    if (
        pending_teachers.find_one({"employee_id": employee_id}) or
        approved_teachers.find_one({"employee_id": employee_id}) or
        rejected_teachers.find_one({"employee_id": employee_id})
    ):
        raise HTTPException(status_code=400, detail="Employee ID already registered or request pending/rejected.")

    pending_teachers.insert_one(teacher_data)
    return {"message": "Registration request submitted"}