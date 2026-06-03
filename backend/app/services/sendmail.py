import os
import resend
from pydantic import EmailStr
from dotenv import load_dotenv
from typing import Dict

load_dotenv()
resend.api_key = os.getenv('RESEND_API_KEY')

# I'm using Resend to send emails. 
# You can find more about it here: https://resend.com/docs/
def send_mail(
    email: EmailStr,
    subject: str,
    html: str,
) -> Dict:
    try:
        params: resend.Emails.SendParams = {
            "from": "Social App <email@stacksnap.dev>",
            "to": [email],
            "subject": subject,
            "html": f"<strong>{html}</strong>",
        }
        email: resend.Emails.SendResponse = resend.Emails.send(params)

        print(email)
        return email
    
    except Exception as e:
        print(f"Error sending email: {e}")
        return {"error": str(e)}
    