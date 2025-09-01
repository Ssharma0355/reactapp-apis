import random
import smtplib
from email.mime.text import MIMEText

def generate_otp():
    return str(random.randint(100000, 999999))

def send_email(to_email: str, otp: str):
    sender = "your-email@gmail.com"
    password = "your-app-password"  # Use App Password for Gmail

    msg = MIMEText(f"Your OTP code is {otp}")
    msg["Subject"] = "Verify your email"
    msg["From"] = sender
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, [to_email], msg.as_string())
    except Exception as e:
        print("Error sending email:", e)
