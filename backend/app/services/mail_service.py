import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydantic import EmailStr
from typing import Dict
from app.config.settings import settings

def send_mail(
    recipient_email: EmailStr,
    subject: str,
    body: str,
    otp: str
) -> None:
    msg = MIMEMultipart()

    msg['from'] = settings.SENDER_EMAIL
    msg['to'] = recipient_email
    msg['Subject'] = subject

    html_content: str = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body style="font-family: sans-serif; padding: 20px; color: #333;">
            <p style="font-size: 16px; line-height: 1.5;">
                <span style="font-weight: bold; color: #5f6368;">{body}</span>
            </p>

            <h1 style="font-size: 32px; letter-spacing: 2px; color: #1a73e8; text-align: center;">{otp}</h1>
        </body>
        </html>
    """

    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        # Connect to the gmail server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(settings.SENDER_EMAIL, settings.SENDER_PASSWORD)
            server.send_message(msg)

        print(f"Email sent successfully to {recipient_email}")
    
    except Exception as e:
        print(f"Error sending email: {e}")
