from app.schemas.auth import SignUp
from app.config.appwrite import users_service, account
from app.services.db import save_user_to_db
from appwrite.id import ID
from app.services.mail_service import send_mail
from pydantic import EmailStr

def create_account(payload: SignUp) -> dict[str, str]:
    # Create the user account in Appwrite auth
    new_user = users_service.create(
        user_id = ID.unique(),
        email = payload.email,
        password = payload.password,
        name = payload.name
    )

    generated_user_id = new_user.id

    # Create the user document and save to db
    save_user_to_db(payload, user_id=generated_user_id)

    return generated_user_id     

def send_verification_otp(user_id: str, email: EmailStr) -> None:
    try:
        token = users_service.create_token(user_id, 6, 300)
        send_mail(
            email,
            "Email Verification OTP",
            "Your OTP for email verification is: ",
            token.secret
        )

        print(f"Verification OTP sent successfully to user ID: {token}")
    except Exception as e:
        print(f"Error sending verification OTP: {e}")
