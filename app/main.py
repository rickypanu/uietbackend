from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .api import admin, register, auth
from app.api import teacher, student, subjects
from app.core.config import URL

app = FastAPI()

# Ensure upload directory exists
os.makedirs("uploads/notifications", exist_ok=True)

# Serve uploaded files
app.mount("/files/notifications", StaticFiles(directory="uploads/notifications"), name="notifications")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(teacher.router)
app.include_router(student.router)
app.include_router(subjects.router)

@app.get("/")
def root():
    return {"message": "College Management API success"}
