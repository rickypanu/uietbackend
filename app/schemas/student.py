from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
import re
from enum import Enum

class Course(str, Enum):
    BE = "BE"
    ME = "ME"

class StudentRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    dob: date
    gender: str
    address: str
    roll_no: str  # Use plain string, not constr
    department: str
    course: str
    branch: str
    semester: int
    section: str

    @field_validator("roll_no")
    @classmethod
    def validate_roll_no(cls, v: str) -> str:
        if not v.isdigit() or len(v) != 6:
            raise ValueError("Roll number must be exactly 6 digits.")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = re.sub(r"[+\-\s]", "", v)
        if cleaned.startswith("91"):
            cleaned = cleaned[2:]
        elif cleaned.startswith("0"):
            cleaned = cleaned[1:]
        if not re.fullmatch(r"\d{10}", cleaned):
            raise ValueError("Phone number must contain exactly 10 digits after removing prefix.")
        return cleaned
