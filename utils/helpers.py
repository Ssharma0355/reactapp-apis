import random, smtplib, ssl, os
from fastapi import HTTPException
from passlib.context import CryptContext
from email.mime.text import MIMEText

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def send_email_otp(to_email: str, otp: str):
    smtp_server = "smtp.gmail.com"
    port = 465
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "Signup OTP Verification"
    msg["From"] = sender_email
    msg["To"] = to_email

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, to_email, msg.as_string())
    except Exception as e:
        print("Error sending email:", e)
        raise HTTPException(status_code=500, detail="Failed to send email")

    smtp_server = "smtp.gmail.com"
    port = 465
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "Signup OTP Verification"
    msg["From"] = sender_email
    msg["To"] = to_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, msg.as_string())
