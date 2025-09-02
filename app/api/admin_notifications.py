# app/api/admin_notifications.py
import os
import shutil
from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
from fastapi.responses import FileResponse
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from typing import Optional, List

# MongoDB Connection
client = MongoClient(os.getenv("MONGO_URI", "mongodb+srv://<your-uri>"))
db = client["uietattendance"]
notifications_col = db["adminnotifications"]

# Router
router = APIRouter(prefix="/admin", tags=["Admin Notifications"])

# Upload folder
UPLOAD_FOLDER = "uploads/notifications"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def notif_serializer(notif) -> dict:
    return {
        "_id": str(notif["_id"]),
        "admin_id": notif["admin_id"],
        "message": notif["message"],
        "category": notif["category"],
        "target_type": notif["target_type"],
        "branch": notif.get("branch", ""),
        "section": notif.get("section", ""),
        "semester": notif.get("semester", ""),
        "roll_numbers": notif.get("roll_numbers", []),
        "expiry_time": notif["expiry_time"],
        "file_url": notif.get("file_url", None),
    }


@router.post("/send-notification")
async def send_notification(
    admin_id: str = Form(...),
    message: str = Form(...),
    category: str = Form(...),
    target_type: str = Form(...),
    expiry_time: str = Form(...),
    branch: Optional[str] = Form(""),
    section: Optional[str] = Form(""),
    semester: Optional[str] = Form(""),
    roll_numbers: Optional[str] = Form(""),
    file: Optional[UploadFile] = None,
):
    try:
        # File Handling
        file_url = None
        if file:
            filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            with open(filepath, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_url = f"/files/notifications/{filename}"

        # Parse roll numbers
        roll_list = []
        if target_type == "individual" and roll_numbers:
            roll_list = [r.strip().upper() for r in roll_numbers.split(",") if r.strip()]

        # Save notification
        notif = {
            "admin_id": admin_id.upper(),
            "message": message,
            "category": category,
            "target_type": target_type,
            "branch": branch,
            "section": section,
            "semester": semester,
            "roll_numbers": roll_list,
            "expiry_time": expiry_time,
            "file_url": file_url,
            "created_at": datetime.utcnow(),
        }
        result = notifications_col.insert_one(notif)

        return {"status": "success", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notifications/{admin_id}")
async def get_notifications(admin_id: str):
    notifs = notifications_col.find({"admin_id": admin_id.upper()}).sort("created_at", -1)
    return [notif_serializer(n) for n in notifs]


@router.post("/notifications/delete")
async def delete_notification(
    notification_id: str = Form(...), admin_id: str = Form(...)
):
    notif = notifications_col.find_one({"_id": ObjectId(notification_id)})
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    if notif["admin_id"] != admin_id.upper():
        raise HTTPException(status_code=403, detail="Not authorized to delete this notification")

    # Delete file if exists
    if notif.get("file_url"):
        filename = notif["file_url"].split("/")[-1]
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    notifications_col.delete_one({"_id": ObjectId(notification_id)})
    return {"status": "success", "message": "Notification deleted"}


# File serving
from fastapi import FastAPI

app = FastAPI()

@app.get("/files/notifications/{filename}")
async def get_file(filename: str):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath)
