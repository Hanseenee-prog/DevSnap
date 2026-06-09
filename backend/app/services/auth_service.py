from turtle import up
from app.schemas.auth import SignUp
from app.config.appwrite import users_service
from app.services.db import get_otp_metadata, save_user_to_db, update_otp_metadata, store_otp_metadata
from app.services.users_service import get_user_account
from appwrite.id import ID
from app.services.mail_service import send_mail
from pydantic import EmailStr
from fastapi import HTTPException, status
from app.services.utils import check_elapsed_time

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
    save_user_to_db(payload, generated_user_id)

    return generated_user_id     

def send_verification_otp(user_id: str, email: EmailStr) -> None:
    # Check if user exists
    user_account = get_user_account(user_id)
    print(f"User Account: {user_account.name}")

    # If the user does not exist, we want to stop here
    if not user_account:
        print(f"User with ID {user_id} does not exist.")
        return None

    try:
        result = get_otp_metadata(user_id)

        # If user id has an already existing metadata, we can just update its info 
        # Else we want to create it for the first time
        if result:
            elapsed = check_elapsed_time(result)

            if elapsed < 60:
                print(F"Please wait {(60 - elapsed):.1f} seconds before requesting a new OTP.")

                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
                    detail=f"OTP was sent less than a minute ago. Please wait {60 - elapsed} seconds before requesting a new OTP."
                )

            # Updates the otp metadata if the user has already requested an OTP before
            update_otp_metadata(user_id)
            

        token = users_service.create_token(user_id, 6, 300)

        if token:
            # Store user to track if the user has requested an OTP before
            if not result:
                store_otp_metadata(user_id)

            send_mail(
                email,
                "Email Verification OTP",
                f"Hi {user_account.name}, Your OTP for email verification is: ",
                token.secret
            )

    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        print(f"Error sending verification OTP: {e}")
