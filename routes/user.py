from fastapi import APIRouter, HTTPException
from config.db import users_collection
from models.user import UserSignup, VerifyOTP
from utils.otp import generate_otp, send_email
from passlib.hash import bcrypt
import datetime

user = APIRouter()

@user.post("/signup")
async def signup(user_data: UserSignup):
    # Check if user already exists
    if users_collection.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hash(user_data.password)
    otp = generate_otp()

    users_collection.insert_one({
        "firstname": user_data.firstname,
        "lastname": user_data.lastname,
        "email": user_data.email,
        "password": hashed_password,
        "otp": otp,
        "otp_expiry": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        "is_verified": False
    })

    send_email(user_data.email, otp)
    return {"message": "User created. Please verify OTP sent to email."}

@user.post("/verify-otp")
async def verify_otp(data: VerifyOTP):
    user = users_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.get("is_verified"):
        return {"message": "User already verified"}

    if "otp" not in user or "otp_expiry" not in user:
        raise HTTPException(status_code=400, detail="OTP not generated. Please request resend.")

    if user["otp"] != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if datetime.datetime.utcnow() > user["otp_expiry"]:
        raise HTTPException(status_code=400, detail="OTP expired")

    users_collection.update_one(
        {"email": data.email},
        {"$set": {"is_verified": True}, "$unset": {"otp": "", "otp_expiry": ""}}
    )

    return {"message": "Email verified successfully. User onboarded!"}

    user = users_collection.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user["otp"] != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if datetime.datetime.utcnow() > user["otp_expiry"]:
        raise HTTPException(status_code=400, detail="OTP expired")

    users_collection.update_one(
        {"email": data.email},
        {"$set": {"is_verified": True}, "$unset": {"otp": "", "otp_expiry": ""}}
    )

    return {"message": "Email verified successfully. User onboarded!"}
