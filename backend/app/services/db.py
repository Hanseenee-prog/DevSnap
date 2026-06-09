from app.config.appwrite import users_service, tables_db
from app.config.settings import settings
from appwrite.query import Query
import uuid

# Function to check if a user exists in Appwrite Auth store
def get_user_by_email(email: str) -> dict | None:
    try:
        result = users_service.list(
            queries=[Query.equal("email", email)]
        )

        if result.total > 0:
            user = result.users[0]
            return user
        return None
    except Exception as e:
        # Logs connection or route errors and defaults safely to None
        print(f"Error checking user email: {e}")
        return None

# Function to save a user to the database
def save_user_to_db(user, user_id) -> None:
    try:
        response = tables_db.create_row(
            database_id = settings.DATABASE_ID,
            table_id = settings.APPWRITE_USERS_COLLECTION_ID,
            row_id = user_id,
            data = {
                "email": user.email,
                "name": user.name,
            }
        )

        print(f"Document created successfully: {response}")
        return { "message": "User document created"}
    
    except Exception as e:
        print(f"Error saving user to database: {e}")

### OTP OPERATIONS

def get_otp_metadata(user_id: str) -> dict | None:
    try:
        result = tables_db.list_rows(
            database_id = settings.DATABASE_ID,
            table_id = settings.APPWRITE_OTP_METADATA_COLLECTION_ID,
            queries = [Query.equal("user_id", user_id)]
        )

        if result and result.total > 0:
            otp_metadata = result.rows[0]
            print(f"Your otp metadata {otp_metadata}")
            return otp_metadata
        return None
    
    except Exception as e:
        print(f"Error retrieving OTP metadata: {e}")
        return None

def store_otp_metadata(user_id: str) -> None:
    try:
        response = tables_db.create_row(
            database_id = settings.DATABASE_ID,
            table_id = settings.APPWRITE_OTP_METADATA_COLLECTION_ID,
            row_id = user_id,
            data = {
                "user_id": user_id,
                "dummy_id": str(uuid.uuid4()), # for tracking changes
            }
        )

        print(f"OTP metadata stored successfully: {response}")
    
    except Exception as e:
        print(f"Error storing OTP metadata: {e}")

def update_otp_metadata(user_id: str) -> None:
    try:
        response = tables_db.update_row(
            database_id = settings.DATABASE_ID,
            table_id = settings.APPWRITE_OTP_METADATA_COLLECTION_ID,
            row_id = user_id,
            data = {
                "dummy_id": str(uuid.uuid4()), # for tracking changes
            }
        )

        print(f"OTP metadata updated successfully: {response}")

    except Exception as e:
        print(f"Error updating OTP metadata: {e}")