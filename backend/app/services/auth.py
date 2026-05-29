from fastapi import HTTPException, status, APIRouter, Depends
from app.schemas.auth import SignUp, SignIn
from app.config.appwrite import client, databases
from appwrite.services.users import Users
# from appwrite.services.account import Account
from app.services.db import get_user_by_email, save_user_to_db
from appwrite.models import User
from appwrite.id import ID

# Set session for the client to manage user sessions
client.set_session('')  

users_service = Users(client)

router = APIRouter()

# User enters full name and email
# Check if the user exists or not (to create a user document or not)
# Send OTP to user's email
# This will send a secret key for creating a session
# Createa new user document if the user is new
# Return the user's accountID that would be used to complete the login
# Verify OTP and authenticate to login

@router.post("/")
def sign_up(payload: SignUp) -> dict[str, str]:
    # Check if the user exists or not (to create a user document or not)
    existing_user = get_user_by_email(payload.email)

    if existing_user:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="An account with this email address already exists."
        )

    try:
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

        return {
            "verification_status": "pending",
            "message": "User created successfully",
            "user_id": generated_user_id
        }       
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Registration execution pipeline failed: {str(e)}"
        )