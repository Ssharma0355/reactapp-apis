from fastapi import APIRouter, HTTPException
from config.db import users_collection
from models.user import UserSignup, VerifyOTP
from utils.otp import generate_otp, send_email_otp   # ✅ use the new function
from passlib.hash import bcrypt
import datetime

user = APIRouter()

@user.post("/signup")
async def signup(user_data: UserSignup):
    if users_collection.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hash(user_data.password)
    otp = generate_otp()

    try:
        send_email_otp(user_data.email, otp)   # ✅ fixed here
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending OTP: {e}")

    users_collection.insert_one({
        "firstname": user_data.firstname,
        "lastname": user_data.lastname,
        "email": user_data.email,
        "password": hashed_password,
        "otp": otp,
        "otp_expiry": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        "is_verified": False
    })

    return {"message": "User created. Please verify OTP sent to email."}


@user.post("/verify-otp")
async def verify_otp(data: VerifyOTP):
    user = users_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.get("is_verified"):
        return {"message": "User already verified"}

    if user.get("otp") != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if datetime.datetime.utcnow() > user["otp_expiry"]:
        raise HTTPException(status_code=400, detail="OTP expired")

    users_collection.update_one(
        {"email": data.email},
        {"$set": {"is_verified": True}, "$unset": {"otp": "", "otp_expiry": ""}}
    )

    return {"message": "Email verified successfully. User onboarded!"}


@user.get("/users")
async def get_allusers():
    users = list(users_collection.find({}, {"password": 0, "otp": 0, "otp_expiry": 0}))
    for user_doc in users:
        user_doc["_id"] = str(user_doc["_id"])
    return {"users": users}


@user.post("/resend-otp")
async def resend_otp(email: str):
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.get("is_verified"):
        return {"message": "User already verified"}

    otp = generate_otp()
    try:
        send_email_otp(email, otp)   # ✅ fixed here
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending OTP: {e}")

    users_collection.update_one(
        {"email": email},
        {"$set": {"otp": otp, "otp_expiry": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}}
    )

    return {"message": "OTP resent successfully"}
