from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import tempfile
import os
from datetime import datetime
from app.db.database import (
    pending_students, approved_students, rejected_students,
    pending_teachers, approved_teachers, rejected_teachers
)

router = APIRouter()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "../static/templates")


def check_existing(field_name: str, value: str, collections: list):
    for collection, status in collections:
        if collection.find_one({field_name: value}):
            return status
    return None


@router.get("/admin/download/student_template")
async def download_student_template():
    file_path = os.path.join(TEMPLATE_DIR, "students_template.xlsx")
    return FileResponse(file_path, filename="students_template.xlsx")

@router.get("/admin/download/teacher_template")
async def download_teacher_template():
    file_path = os.path.join(TEMPLATE_DIR, "teachers_template.xlsx")
    return FileResponse(file_path, filename="teachers_template.xlsx")



@router.post("/admin/register/bulk_students")
async def bulk_register_students(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        suffix = os.path.splitext(file.filename)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Read Excel/CSV
        df = pd.read_excel(tmp_path) if suffix in [".xls", ".xlsx"] else pd.read_csv(tmp_path)

        results = []
        collections = [
            (pending_students, "pending"),
            (approved_students, "approved"),
            (rejected_students, "rejected"),
        ]

        for _, row in df.iterrows():
            full_name = str(row.get("name", "")).strip()
            email = str(row.get("email", "")).strip()
            phone = str(row.get("phone", "")).strip()
            roll_no = str(row.get("roll_no", "")).strip()

            try:
                # Validation
                for field in ["roll_no", "phone", "email"]:
                    status = check_existing(field, row.get(field), collections)
                    if status:
                        results.append({
                            "Roll No": roll_no,
                            "Name": full_name,
                            "Status": "Failed",
                            "Reason": f"{field} already exists ({status})"
                        })
                        raise Exception("skip insert")

                # Insert into pending
                # student_data = row.to_dict()
                # student_data["dob"] = str(student_data.get("dob", ""))
                # approved_students.insert_one(student_data)

                # For Students
                student_data = row.to_dict()

                # Rename "name" column to "full_name"
                if "name" in student_data:
                    student_data["full_name"] = str(student_data.pop("name", "")).strip()

                # Format DOB as YYYY-MM-DD only
                dob_val = student_data.get("dob", "")

                if pd.notna(dob_val) and dob_val != "":
                    try:
                        student_data["dob"] = pd.to_datetime(dob_val).strftime("%Y-%m-%d")
                    except Exception:
                        student_data["dob"] = str(dob_val)
                else:
                    student_data["dob"] = ""

                approved_students.insert_one(student_data)


                results.append({
                    "Roll No": roll_no,
                    "Name": full_name,
                    "Status": "Registered",
                    "Reason": "-"
                })

            except Exception as e:
                if "skip insert" not in str(e):
                    results.append({
                        "Roll No": roll_no,
                        "Name": full_name,
                        "Status": "Failed",
                        "Reason": str(e)
                    })

        # Save results to Excel
        result_df = pd.DataFrame(results)
        output_path = os.path.join(tempfile.gettempdir(), f"students_result_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx")
        result_df.to_excel(output_path, index=False)

        return FileResponse(output_path, filename="students_result.xlsx")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/admin/register/bulk_teachers")
async def bulk_register_teachers(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        suffix = os.path.splitext(file.filename)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Read Excel/CSV
        df = pd.read_excel(tmp_path) if suffix in [".xls", ".xlsx"] else pd.read_csv(tmp_path)

        results = []
        collections = [
            (pending_teachers, "pending"),
            (approved_teachers, "approved"),
            (rejected_teachers, "rejected"),
        ]

        for _, row in df.iterrows():
            full_name = str(row.get("name", "")).strip()
            email = str(row.get("email", "")).strip()
            phone = str(row.get("phone", "")).strip()
            emp_id = str(row.get("employee_id", "")).strip()

            try:
                # Validation
                for field in ["employee_id", "phone", "email"]:
                    status = check_existing(field, row.get(field), collections)
                    if status:
                        results.append({
                            "Employee ID": emp_id,
                            "Name": full_name,
                            "Status": "Failed",
                            "Reason": f"{field} already exists ({status})"
                        })
                        raise Exception("skip insert")

                # Insert into pending
                # teacher_data = row.to_dict()
                # teacher_data["dob"] = str(teacher_data.get("dob", ""))
                # approved_teachers.insert_one(teacher_data)

                teacher_data = row.to_dict()

                # Rename name → full_name
                if "name" in teacher_data:
                    teacher_data["full_name"] = str(teacher_data.pop("name", "")).strip()

                # Format DOB as YYYY-MM-DD only
                dob_val = teacher_data.get("dob", "")
                if pd.notna(dob_val) and dob_val != "":
                    try:
                        teacher_data["dob"] = pd.to_datetime(dob_val).strftime("%Y-%m-%d")
                    except Exception:
                        teacher_data["dob"] = str(dob_val)
                else:
                    teacher_data["dob"] = ""

                approved_teachers.insert_one(teacher_data)

                results.append({
                    "Employee ID": emp_id,
                    "Name": full_name,
                    "Status": "Registered",
                    "Reason": "-"
                })

            except Exception as e:
                if "skip insert" not in str(e):
                    results.append({
                        "Employee ID": emp_id,
                        "Name": full_name,
                        "Status": "Failed",
                        "Reason": str(e)
                    })

        # Save results to Excel
        result_df = pd.DataFrame(results)
        output_path = os.path.join(tempfile.gettempdir(), f"teachers_result_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx")
        result_df.to_excel(output_path, index=False)

        return FileResponse(output_path, filename="teachers_result.xlsx")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
