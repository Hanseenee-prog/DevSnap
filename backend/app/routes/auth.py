from fastapi import APIRouter, HTTPException, status
from app.services.db import get_user_by_email
from app.config.appwrite import users_service, account
from app.schemas.auth import SignUp, SignIn
from app.services.auth_service import create_account, send_verification_otp

router = APIRouter()

@router.post("/signup", tags=["Sign up"])
def sign_up(payload: SignUp) -> dict[str, str]:
    # Check if the user exists or not (to create a user document or not)
    existing_user = get_user_by_email(payload.email)

    if existing_user:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="An account with this email address already exists."
        )

    try:
        # Create the user account in Appwrite auth and save to db
        new_user_id = create_account(payload)

        if new_user_id:
            otp = send_verification_otp(new_user_id, payload.email)

        return {
            "message": f"User created successfully. Please verify your email to complete the registration process. {otp}",
            "verification_status": "pending",
            "user_id": new_user_id
        }     
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Registration execution pipeline failed: {str(e)}"
        )

@router.post("/verify-email", tags=["Verify email"])
def verify_email(user_id: str, otp: str) -> dict[str, str]:
    try:
        # create a session for the user after verifying the otp
        session = account.create_session(user_id, otp)

        # Update email verification status
        if session:
            users_service.update_email_verification(user_id, True)

        return { 
            "userId": user_id,
            "sessionId": session.id,
            "message": "Email verified successfully. You are now logged in.",
            "verification_status": "true"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Email verification failed: {str(e)}"
        )

@router.post("/signin", tags=["Sign in"])
def signin(payload: SignIn):
    # Check if the email exists
    existing_user = get_user_by_email(payload.email)

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"This email does not exist. Please create an account."
        )

    try:
        # Validate password by creating a session
        session = account.create_email_password_session(payload.email, payload.password)

        print(f"user id: {session.userid}, session id: {session.id}")

        return {
            "user_id": session.userid,
            "sessionId": session.id,
            "message": "Signin successful."
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Sign in failed: {str(e)}"
        )

@router.post("/signout", tags=["Sign Out"])
def sign_out(user_id: str, session_id: str):
    try:
        # Delete the session
        users_service.delete_session(user_id, session_id)
        return { "message": "Logout successful" }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to logout {str(e)}"
        )