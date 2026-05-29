from app.config.appwrite import client, databases, users_service
from app.config.settings import settings
from appwrite.query import Query
from datetime import datetime, timezone

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
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        databases.create_document(
            database_id = settings.DATABASE_ID,
            collection_id = settings.APPWRITE_USERS_COLLECTION_ID,
            document_id = user_id,
            data = {
                "email": user.email,
                "name": user.name,
                "gender": "",
                "bio": "",
            }
        )

        return { "message": "User document created"}
    except Exception as e:
        print(f"Error saving user to database: {e}")