import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL") 
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_ID = os.getenv("ADMIN_ID")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
URL = os.getenv("url")


SUBJECTS = {
    "CSE": {
        "1": ["Maths", "Physics"],
        "2": ["DSA", "OOP"],
        "3": ["DBMS", "OS"],
    },
    "ECE": {
        "1": ["Basic Electronics", "Maths"],
        "2": ["EMT", "Digital"],
        "3": ["DSP", "VLSI"],
    },
    "MECH": {
        "1": ["Mechanics", "Maths"],
        "2": ["Thermodynamics", "Fluid Mechanics"],
    },
}



