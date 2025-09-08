from fastapi import APIRouter, HTTPException
from config.db import users_collection
from models.user import UserSignup, VerifyOTP, UserLogin, HiringOnboarding, CandidateOnboarding
from utils.otp import generate_otp, send_email_otp
from bson import ObjectId
from passlib.context import CryptContext
import datetime
from pydantic import BaseModel

user = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==========================
# Signup
# ==========================
@user.post("/signup")
async def signup(user_data: UserSignup):
    if users_collection.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user_data.password)
    otp = generate_otp()

    try:
        send_email_otp(user_data.email, otp)
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


# ==========================
# Verify OTP
# ==========================
@user.post("/verify-otp")
async def verify_otp(data: VerifyOTP):
    user_doc = users_collection.find_one({"email": data.email})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    if user_doc.get("is_verified"):
        return {"message": "User already verified"}

    if user_doc.get("otp") != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if datetime.datetime.utcnow() > user_doc["otp_expiry"]:
        raise HTTPException(status_code=400, detail="OTP expired")

    users_collection.update_one(
        {"email": data.email},
        {"$set": {"is_verified": True}, "$unset": {"otp": "", "otp_expiry": ""}}
    )

    return {"message": "Email verified successfully. User onboarded!"}


# ==========================
# Resend OTP
# ==========================
class ResendOTP(BaseModel):
    email: str

@user.post("/resend-otp")
async def resend_otp(data: ResendOTP):
    user_doc = users_collection.find_one({"email": data.email})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    if user_doc.get("is_verified"):
        return {"message": "User already verified"}

    otp = generate_otp()
    try:
        send_email_otp(data.email, otp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending OTP: {e}")

    users_collection.update_one(
        {"email": data.email},
        {"$set": {
            "otp": otp,
            "otp_expiry": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        }}
    )

    return {"message": "OTP resent successfully"}


# ==========================
# Get All Users
# ==========================
@user.get("/users")
async def get_allusers():
    users = list(users_collection.find({}, {"password": 0, "otp": 0, "otp_expiry": 0}))
    for user_doc in users:
        user_doc["_id"] = str(user_doc["_id"])  # convert ObjectId to string
    return {"users": users}


# ==========================
# Get User By ID
# ==========================
@user.get("/users/{user_id}")
async def get_user_by_id(user_id: str):
    try:
        obj_id = ObjectId(user_id)  # convert string to ObjectId
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    user_doc = users_collection.find_one(
        {"_id": obj_id},
        {"password": 0, "otp": 0, "otp_expiry": 0}  # hide sensitive fields
    )
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    user_doc["_id"] = str(user_doc["_id"])  # convert ObjectId to string
    return {"user": user_doc}


# ==========================
# Login
# ==========================
@user.post("/login")
async def login(user_data: UserLogin):
    user_doc = users_collection.find_one({"email": user_data.email})
    if not user_doc:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not user_doc.get("is_verified"):
        raise HTTPException(status_code=403, detail="Please verify your email first")

    if not pwd_context.verify(user_data.password, user_doc["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"message": "Login successful", "email": user_doc["email"]}

# ==========================
# Onboarding Routes will be added here later
# ==========================    
@user.post("/onboarding/hiring")
async def hiring_onboarding(data: HiringOnboarding):
    user_doc = users_collection.find_one({"email": data.email})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    if not user_doc.get("is_verified"):
        raise HTTPException(status_code=403, detail="Please verify email first")

    users_collection.update_one(
        {"email": data.email},
        {"$set": {"onboarding_type": "hiring", "hiring_details": data.dict()}}
    )

    return {"message": "Hiring details saved successfully"}
# ==========================
# Onboarding Routes will be added here later
# ==========================    

@user.post("/onboarding/candidate")
async def candidate_onboarding(data: CandidateOnboarding):
    user_doc = users_collection.find_one({"email": data.email})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    if not user_doc.get("is_verified"):
        raise HTTPException(status_code=403, detail="Please verify email first")

    users_collection.update_one(
        {"email": data.email},
        {"$set": {"onboarding_type": "candidate", "candidate_details": data.dict()}}
    )

    return {"message": "Candidate details saved successfully"}