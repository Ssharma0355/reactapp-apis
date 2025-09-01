from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

class GetAllUsets(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr