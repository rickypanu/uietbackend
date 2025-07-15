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


SUBJECTS = [
    "EMT", "VLSI", "DSA", "CE",
    "DSP", "Analog Electronics",
    "MICROPROCESSOR", "Communication Systems",
    "NETWORKS", "AI"
]


