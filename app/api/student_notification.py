# app/api/student_notifications.py
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from datetime import datetime
import os

client = MongoClient(os.getenv("MONGO_URI", "mongodb+srv://<your-uri>"))
db = client["uietattendance"]

teacher_notifications = db["notifications"]
admin_notifications = db["adminnotifications"]

router = APIRouter(prefix="/student", tags=["Student Notifications"])


def safe_datetime(value):
    """Convert MongoDB date, epoch, or string → datetime"""
    if isinstance(value, datetime):
        return value
    if isinstance(value, dict) and "$date" in value:
        return datetime.fromtimestamp(int(value["$date"]["$numberLong"]) / 1000)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000 if value > 1e12 else value)
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except:
            return datetime.utcnow()
    return datetime.utcnow()


def teacher_notif_serializer(n):
    return {
        "_id": str(n["_id"]),
        "source": "teacher",
        "teacher_name": n.get("teacher_name", f"Teacher {n.get('sender_id', '')}"),
        "message": n.get("message", ""),
        "file_url": n.get("file_url"),
        "timestamp": safe_datetime(n.get("timestamp", datetime.utcnow())),
        "expiry_time": safe_datetime(n.get("expiry_time", datetime.utcnow())),
        "branch": n.get("target_branch", ""),
        "section": n.get("target_section", ""),
        "semester": n.get("target_semester", ""),
    }


def admin_notif_serializer(n):
    return {
        "_id": str(n["_id"]),
        "source": "admin",
        "teacher_name": "Admin",
        "message": n.get("message", ""),
        "file_url": n.get("file_url"),
        "timestamp": safe_datetime(n.get("created_at", datetime.utcnow())),
        "expiry_time": safe_datetime(n.get("expiry_time", datetime.utcnow())),
        "branch": n.get("branch", ""),
        "section": n.get("section", ""),
        "semester": n.get("semester", ""),
    }


@router.get("/notifications/{branch}/{section}/{semester}/{roll_no}")
async def get_student_notifications(branch: str, section: str, semester: str, roll_no: str):
    try:
        now = datetime.utcnow()

        # Teacher notifications
        # t_query = {
        #     "$or": [
        #         {"target_branch": branch, "target_section": section, "target_semester": semester},
        #         {"target_type": "all"},
        #         {"target_type": "individual", "roll_numbers": {"$in": [roll_no.upper()]}},
        #     ]
        # }
        # Teacher notifications
        t_query = {
            "$or": [
                # Match teacher’s branch/section/semester
                {
                    "target_branch": branch,
                    "target_section": section,
                    "target_semester": semester,
                },
                # If you later add support for global/individual targeting in teacher notifs
                {"target_type": "all"},
                {"target_type": "individual", "roll_numbers": {"$in": [roll_no.upper()]}}
            ]
        }

        t_notifs = teacher_notifications.find(t_query)

        # Admin notifications
        a_query = {
            "$or": [
                {"target_type": "all"},
                {"target_type": "class", "branch": branch, "section": section, "semester": semester},
                {"target_type": "individual", "roll_numbers": {"$in": [roll_no.upper()]}},
            ]
        }
        a_notifs = admin_notifications.find(a_query)

        merged = []

        # Serialize teacher notifs
        for n in t_notifs:
            data = teacher_notif_serializer(n)
            if data["expiry_time"] > now:
                merged.append(data)

        # Serialize admin notifs
        for n in a_notifs:
            data = admin_notif_serializer(n)
            if data["expiry_time"] > now:
                merged.append(data)

        # Sort latest first
        merged.sort(key=lambda x: x["timestamp"], reverse=True)

        return merged
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
