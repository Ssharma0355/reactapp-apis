import random, smtplib, ssl, os
from fastapi import HTTPException
from passlib.context import CryptContext
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

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

    if not sender_email or not password:
        raise HTTPException(status_code=500, detail="Email credentials not set")

    # ✨ Improved email content
    email_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height:1.6; color:#333;">
            <h2 style="color:#4CAF50;">Welcome to Hustle Dream 🚀</h2>
            <p>Hey there,</p>
            <p>We’re excited to have you join us on this journey! Before we kick off the onboarding process, we just need to verify your email.</p>
            <p style="font-size:16px; font-weight:bold; color:#2c3e50;">
                🔐 Your OTP is: <span style="color:#e67e22;">{otp}</span>
            </p>
            <p>Please enter this OTP in the app to complete your signup.</p>
            <br>
            <p>Cheers,<br>The Hustle Dream Team 💡</p>
        </body>
    </html>
    """

    msg = MIMEText(email_body, "html")
    msg["Subject"] = "✨ Welcome to Hustle Dream - Verify Your OTP"
    msg["From"] = sender_email
    msg["To"] = to_email

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"✅ OTP {otp} sent to {to_email}")
    except Exception as e:
        print("❌ Error sending email:", e)
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
