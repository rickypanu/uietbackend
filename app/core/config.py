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
        "1": ["Calculus", "Physics", "Professional Communication","Workshop" , "Programming Fundamentals", "UHV"],
        "2": ["Basic Electrical and Electronics Engineering", "Applied Chemistry", "Engineering Graphics", "OOPs", "Differential Equations and Transforms"],
        "3": ["DBMS", "Data Structure", "Discrete Systems", "Web Technologies", "Software Technologies"],
        "4": [""],
        "5": ["Computer Graphics", "Theory of Computation", "Artificial Intelligence", "Natural language Processing","Economics"],
        "6": [""],
        "7": [""],
        "8": [""],
    },
    "ECE": {
        "1": ["Basic Electrical and Electronics Engineering", "Engineering Graphics", "Applied Chemistry", "Calculus", "Programming Fundamentals", ],
        "2": ["Workshop", "Digital Design", "Professional Communication", "UHV", "Applies Physics"],
        "3": ["Linear Algebra and Complex Analysis", "Signals and Systems", "Microprocessor and Microcontroller", "Electronic Devices and Circuits", "Electronics Measurementsand Instrumentation", "Economics"],
        "4": ["Communication Engineering", "Advance Microcontroller and Application", "Analog Electronics Circuits", "Probability and Random Process", "Electromagnetic Theory", "Network Analysis"],
        "5": ["VLSI", "AWP","DSD","DSA", "DSP", "CN"],
        "6": ["Microwave & Radar Engineering", "Fibre Optic Communication Systems", "Digital Communication", "Control Systems", "Power Electronics", "Satellite Communication" ],
        "7": ["Wireless and Mobile Communication", "Embedded System Design"],
        "8": [""],
    },
    "MECH": {
        "1": ["Mechanics", "Maths"],
        "2": ["Thermodynamics", "Fluid Mechanics"],
        "3": [""],
        "4": [""],
        "5": [""],
        "6": [""],
        "7": [""],
        "8": [""],
    },
}



