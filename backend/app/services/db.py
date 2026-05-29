from app.config.appwrite import users_service, tables_db
from app.config.settings import settings
from appwrite.query import Query

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