from pydantic import BaseModel, EmailStr, field_validator, constr
from typing import Annotated
from datetime import date
import re

class StudentRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    dob: date
    gender: str
    address: str
    roll_no: constr(pattern=r'^\d+$')
    department: str
    course: str
    semester: int
    section: str

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        # Remove +, -, and spaces
        cleaned = re.sub(r'[+\-\s]', '', v)

        # Remove leading '91' or '0'
        if cleaned.startswith('91'):
            cleaned = cleaned[2:]
        elif cleaned.startswith('0'):
            cleaned = cleaned[1:]

        # Must be exactly 10 digits now
        if not re.fullmatch(r'\d{10}', cleaned):
            raise ValueError('Phone number must contain exactly 10 digits after removing prefix')

        return cleaned
