from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
import datetime

class UserSignup(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

class GetAllUsets(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr


class HiringOnboarding(BaseModel):
    email: str
    jobTitle: str
    department: str
    employmentType: str
    experienceLevel: str
    location: str
    remotePolicy: str
    salaryRange: Optional[str] = None
    applicationDeadline: str
    jobDescription: str
    responsibilities: str
    qualifications: str
    benefits: Optional[str] = None
    contactEmail: str
    hiringManager: Optional[str] = None
    companyLogo: Optional[str] = None   # store uploaded logo URL
    jobBanner: Optional[str] = None     # store uploaded banner URL


class CandidateOnboarding(BaseModel):
    email: str
    govtIdType: Optional[str]
    govtIdNumber: Optional[str]
    sex: Optional[str]
    dob: Optional[str]
    nationality: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    experience: Optional[str]
    college: Optional[str]
    degree: Optional[str]
    marks: Optional[str]
    resume: Optional[str] = None        # uploaded resume path
    photo: Optional[str] = None 


class PostCreate(BaseModel):
    author_email: EmailStr
    text: Optional[str] = None
    media: Optional[str] = None   # Path to uploaded file

class Comment(BaseModel):
    user_email: EmailStr
    text: str
    created_at: datetime.datetime = datetime.datetime.utcnow()