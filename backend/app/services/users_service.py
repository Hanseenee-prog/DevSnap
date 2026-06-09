from app.config.appwrite import users_service, tables_db

def get_user_account(user_id: str) -> dict | None:
    try:
        user_account = users_service.get(user_id)
        return user_account
    except Exception as e:
        print(f"Error retrieving user account: {e}")
        return None