from appwrite.services.users import Users
from app.config.appwrite import client, databases
from app.config.settings import settings
from appwrite.query import Query
from datetime import datetime

users = Users(client)

# Function to check if a user exists in the database
def get_user_by_email(email: str) -> dict:
    # Check if a user with the given email exists in the database
    result: dict = users.list(
        queries=[Query.equal("email", email)]
    )

    if result['total'] > 0:
        return result['users'][0]
    else:
        return None

# Function to save a user to the database
def save_user_to_db(user, user_id) -> None:
    try:
        now_iso = datetime.now().isoformat() + "Z"

        databases.create_document(
            database_id = settings.DATABASE_ID,
            collection_id = settings.USER_COLLECTION_ID,
            document_id = user_id,
            data = {
                "email": user.email,
                "name": user.name,
                "gender": "",
                "bio": "",
                "createdAt": now_iso,
                "updatedAt": now_iso
            }
        )
    except Exception as e:
        print(f"Error saving user to database: {e}")