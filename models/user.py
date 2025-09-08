from pydantic import BaseModel, EmailStr, Field
from typing import Optional

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